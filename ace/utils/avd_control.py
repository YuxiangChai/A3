import base64
import json
import logging
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import easyocr
from ace.evaluators import *
from ace.utils.common_utils import check_create_dir, combine_screenshots, parse_xmls
from ace.utils.keycode import KEYCODE
from ace.utils.som import draw_mark
from appium import webdriver
from appium.options.android import UiAutomator2Options


class Controller:
    def __init__(
        self,
        config: dict,
        app_ids: dict,
        logger: logging.Logger,
        appium_port: int = 4723,
        udid: str = None,
    ) -> None:
        if udid is None:
            self.capabilities = dict(
                platformName="Android",
                automationName="uiautomator2",
                deviceName="Android",
                language="en",
                locale="US",
                newCommandTimeout=480,
            )
        else:
            self.capabilities = dict(
                platformName="Android",
                automationName="uiautomator2",
                deviceName=udid,
                udid=udid,
                language="en",
                locale="US",
                newCommandTimeout=480,
            )

        self.appium_server_url = f"http://localhost:{appium_port}"
        self.driver = webdriver.Remote(
            self.appium_server_url,
            options=UiAutomator2Options().load_capabilities(self.capabilities),
        )
        self.driver.implicitly_wait(2)

        wh = self.driver.get_window_size()
        self.w = wh["width"]
        self.h = wh["height"]

        self.history = {
            "xml": [],
            "screenshot": [],
            "ocr_results": [],
            "actions": [],
            "agent_messages": [],
            "achieved_essential_states": {},
        }
        self.app_ids = app_ids
        self.config = config
        self.logger = logger
        self.step = 0

        self.reader = easyocr.Reader(["ch_sim", "en"])

    def _get_xml(self) -> str:
        return self.driver.page_source

    def _get_screenshot(self) -> str:
        """get current screenshot of the device, return a base64 string

        Returns:
            str: a base64 string of the screenshot
        """
        b = self.driver.get_screenshot_as_base64()
        return b

    def _open(self, app: str) -> None:
        """This function is used to directly open an app on the device, following the style of AndroidControl.

        Args:
            app (str): The name of the app.
        """
        if app.lower() == "youtube":
            subprocess.run(
                [
                    "adb",
                    "shell",
                    "monkey",
                    "-p",
                    "com.google.android.youtube",
                    "-c",
                    "android.intent.category.LAUNCHER",
                    "1",
                ],
                stdout=subprocess.DEVNULL,  # Suppress stdout
                stderr=subprocess.DEVNULL,  # Suppress stderr
            )
        else:
            try:
                self.driver.activate_app(self.app_ids[app.lower()])
            except KeyError as e:
                self.logger.log(logging.INFO, e)
                self.logger.log(logging.INFO, f"App {app} not found.")

    def _tap(self, x: int, y: int) -> None:
        self.driver.tap(
            positions=[(x, y)],
            duration=100,
        )

    def _long_press(self, x: int, y: int, duration: int = 1000) -> None:
        self.driver.tap(
            positions=[(x, y)],
            duration=duration,
        )

    def _swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 1000) -> None:
        self.driver.swipe(
            start_x=x1,
            start_y=y1,
            end_x=x2,
            end_y=y2,
            duration=duration,
        )

    def _type(self, text: str) -> None:
        for c in text:
            c = c.upper()
            self.driver.press_keycode(KEYCODE.get(c, KEYCODE["SPACE"]))

    def _enter(self) -> None:
        self.driver.press_keycode(KEYCODE["ENTER"])

    def _back(self) -> None:
        self.driver.press_keycode(KEYCODE["BACK"])

    def _home(self) -> None:
        self.driver.press_keycode(KEYCODE["HOME"])
        time.sleep(1)

    def _all_apps(self) -> None:
        self.driver.press_keycode(KEYCODE["ALL_APPS"])
        time.sleep(1)

    def _wait(self, duration: int = 5) -> None:
        time.sleep(duration)

    def _terminate_all_apps(self) -> None:
        self._home()
        self._all_apps()
        self._swipe(
            int(0.1 * self.w),
            int(0.5 * self.h),
            int(0.9 * self.w),
            int(0.5 * self.h),
            100,
        )
        time.sleep(1)
        self._tap(int(0.2 * self.w), int(0.48 * self.h))
        time.sleep(1.5)

    def _ocr(self, screenshot: bytes) -> list[dict]:
        """perform OCR on the screenshot

        Args:
            screenshot (bytes): bytes of the screenshot

        Returns:
            list[dict]: the OCR results
        """
        result = self.reader.readtext(screenshot)
        ret = []
        for r in result:
            bbox = r[0]
            x1, y1 = int(bbox[0][0]), int(bbox[0][1])
            x2, y2 = int(bbox[2][0]), int(bbox[2][1])
            words = r[1]
            ret.append({"bbox": [x1, y1, x2, y2], "words": words})
        return ret

    def start_record(self, resolution: list[int]) -> None:
        self.driver.start_recording_screen(videoSize=f"{resolution[0]}x{resolution[1]}")

    def stop_save_record(self, save_path: Path) -> None:
        recording = self.driver.stop_recording_screen()
        recording = base64.b64decode(recording)
        with open(save_path / f"task_{self.task_idx}.mp4", "wb") as f:
            f.write(recording)

    def get_state(self) -> dict:
        """get current state of the device

        Returns:
            dict: a dictionary containing the current state of the device
        """
        xml = self._get_xml()
        screenshot = self._get_screenshot()

        return {"xml": xml, "screenshot": screenshot}

    def save_state(self, save_path: Path) -> None:
        screenshot_dir = check_create_dir(save_path / "screenshots")
        xml_dir = check_create_dir(save_path / "xmls")
        state = self.get_state()
        with open(
            screenshot_dir / f"task_{self.task_idx}_step_{self.step}.png", "wb"
        ) as f:
            screenshot = base64.b64decode(state["screenshot"])
            f.write(screenshot)

        with open(xml_dir / f"task_{self.task_idx}_step_{self.step}.xml", "w") as f:
            f.write(state["xml"])

        self.history["screenshot"].append(state["screenshot"])
        self.history["xml"].append(state["xml"])
        if self.config["eval_modality_text"] == "ocr":
            ocr_results = self._ocr(screenshot)
            self.history["ocr_results"].append(ocr_results)

    def get_history(self) -> dict:
        return self.history

    def save_history(self, save_path: Path) -> None:
        history = self.get_history()
        history_ = []

        for i in range(len(history["xml"])):
            history_.append(
                {
                    "task": self.task,
                    "task_level": self.task_level,
                    "category": self.category,
                    "xml": f"task_{self.task_idx}_step_{i}.xml",
                    "screenshot": f"task_{self.task_idx}_step_{i}.png",
                    "ocr_results": (
                        history["ocr_results"][i]
                        if self.config["eval_modality_text"] == "ocr"
                        else []
                    ),
                    "actions": history["actions"][i],
                    "agent_messages": history["agent_messages"][i],
                    "achieved_essential_states": history[
                        "achieved_essential_states"
                    ].get(
                        f"{i-self.config['eval_essential_state_group_steps']}-{i}", {}
                    ),
                }
            )

        with open(save_path / f"task_{self.task_idx}_history.json", "w") as f:
            json.dump(history_, f, indent=2)

    def save_history_agent_message(self, agent_message: str) -> None:
        self.history["agent_messages"].append(agent_message)

    def exe_action(self, action: dict, save_flag: bool = True) -> None:
        """execute action on the device

        Args:
            action (dict): action to be executed
        """
        if action["action"] == "open":
            self._open(action["app"])
        elif action["action"] == "tap":
            self._tap(action["x"], action["y"])
        elif action["action"] == "long_press":
            self._long_press(action["x"], action["y"])
        elif action["action"] == "swipe":
            if "duration" in action:
                self._swipe(
                    action["x1"],
                    action["y1"],
                    action["x2"],
                    action["y2"],
                    action["duration"],
                )
            else:
                self._swipe(action["x1"], action["y1"], action["x2"], action["y2"])
        elif action["action"] == "type":
            self._type(action["text"])
        elif action["action"] == "enter":
            self._enter()
        elif action["action"] == "back":
            self._back()
        elif action["action"] == "home":
            self._home()
        elif action["action"] == "wait":
            self._wait(action["duration"])
        elif action["action"] == "end":
            if self.logger is not None and save_flag:
                self.logger.log(logging.INFO, f"Task Finished.")

        if save_flag:
            self.history["actions"].append(action)
        self.step += 1

    def set_task_eval(
        self,
        task: str,
        task_idx: int,
        task_level: str,
        category: str,
        essential_states: list[str],
    ) -> None:
        """Set the task and evaluation function, which also start a new history.

        Args:
            task (str): task string
            eval (Callable): evaluation function
        """
        self.step = 0
        self.task = task
        self.task_idx = task_idx
        self.essential_states = essential_states
        self.task_level = task_level
        self.category = category
        self.history = {
            "xml": [],
            "screenshot": [],
            "ocr_results": [],
            "actions": [],
            "agent_messages": [],
            "achieved_essential_states": {},
        }

    def eval_final_state_worker(self, evaluator: dict, task: str, history: dict) -> str:
        sk = evaluator["sk"]
        model = evaluator["model"]

        if evaluator["name"] == "gpt":
            final_state_eval = GPTEvaluator(sk=sk, model=model)
        elif evaluator["name"] == "gemini":
            final_state_eval = GeminiEvaluator(sk=sk, model=model)
        elif evaluator["name"] == "claude":
            final_state_eval = ClaudeEvaluator(sk=sk, model=model)
        else:
            raise ValueError(f"Unknown evaluator: {evaluator['name']}")

        if self.config["eval_modality_text"] == "xml":
            elements = parse_xmls([history["xml"][-1]])[0]
        elif self.config["eval_modality_text"] == "ocr":
            elements = self._ocr(history["screenshot"][-1])
        else:
            raise ValueError(
                f"Unknown text modality: {self.config['eval_modality_text']}"
            )

        if self.config["eval_screenshot_som"]:
            screenshot = draw_mark(history["screenshot"][-1], elements)
        else:
            screenshot = base64.b64decode(history["screenshot"][-1])

        response_result = final_state_eval.eval(
            task,
            elements,
            screenshot,
        )

        return response_result

    def eval_final_state(self) -> bool | str:
        """evaluate whether the task is completed correctly based on final state

        Returns:
            bool | str: the evaluation result
        """
        history = self.get_history()

        results = {}
        reasons = {}

        # Run evaluators in parallel
        with ThreadPoolExecutor(max_workers=len(self.config["evaluators"])) as executor:
            future_to_evaluator = {
                executor.submit(
                    self.eval_final_state_worker,
                    evaluator,
                    self.task,
                    history,
                ): evaluator
                for evaluator in self.config["evaluators"]
            }

            # Collect results as they complete
            for future in as_completed(future_to_evaluator):
                evaluator = future_to_evaluator[future]
                try:
                    result = future.result()

                    result_dict = json.loads(result)
                    results[evaluator["name"]] = result_dict["answer"]
                    reasons[evaluator["name"]] = result_dict["reason"]
                except Exception as e:
                    self.logger.error(f"Error with {evaluator['name']}: {e}")
                    results[evaluator["name"]] = "error"
                    reasons[evaluator["name"]] = str(e)

        return results, reasons

    def evaluate_state_worker(
        self,
        evaluator: dict,
        elements: list[dict],
        combined_screenshot: bytes,
        states: list[str],
    ) -> tuple[str, dict]:
        sk = evaluator["sk"]
        model = evaluator["model"]

        if evaluator["name"] == "gpt":
            state_eval = GPTStateEval(sk=sk, model=model)
        elif evaluator["name"] == "gemini":
            state_eval = GeminiStateEval(sk=sk, model=model)
        elif evaluator["name"] == "claude":
            state_eval = ClaudeStateEval(sk=sk, model=model)
        else:
            raise ValueError(f"Unknown evaluator: {evaluator['name']}")

        response_result = state_eval.eval_state(
            xmls=elements,
            screenshots=combined_screenshot,
            states=states,
        )
        # response_result = state_eval.model

        return evaluator["name"], response_result

    def eval_essential_states(self) -> None:
        """evaluate the essential states of the device"""
        self.logger.log(
            logging.INFO, f"Evaluating essential states at step: {self.step}"
        )
        group_steps = self.config["eval_essential_state_group_steps"]
        history = self.get_history()
        screenshots = history["screenshot"][-group_steps:]

        screenshots = [base64.b64decode(screenshot) for screenshot in screenshots]

        combined_screenshot = combine_screenshots(screenshots)
        if self.config["eval_modality_text"] == "xml":
            xmls = history["xml"][-group_steps:]
            elements = parse_xmls(xmls)
        elif self.config["eval_modality_text"] == "ocr":
            elements = history["ocr_results"][-group_steps:]
        else:
            raise ValueError(
                f"Unknown text modality: {self.config['eval_modality_text']}"
            )

        eval_results = {}
        self.achieved_essential_states = {}
        self.unachieved_essential_states = {}
        # Run evaluators in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_evaluator = {
                executor.submit(
                    self.evaluate_state_worker,
                    evaluator,
                    elements,
                    combined_screenshot,
                    self.essential_states,
                ): evaluator
                for evaluator in self.config["evaluators"]
            }

            for future in as_completed(future_to_evaluator):
                evaluator_name, response_result = future.result()
                try:
                    response_result = json.loads(response_result)
                    achieved_essential_states = response_result["states"]
                    answer = response_result.get("answer")
                    reason = response_result["reason"]
                except json.JSONDecodeError:
                    achieved_essential_states = []
                    answer = None
                    reason = response_result

                if eval_results.get(evaluator_name) is None:
                    eval_results[evaluator_name] = []
                eval_results[evaluator_name].append(
                    {
                        "achieved_essential_states": achieved_essential_states,
                        "answer": answer,
                        "reason": reason,
                    }
                )
                self.achieved_essential_states[evaluator_name] = (
                    achieved_essential_states
                )
                self.unachieved_essential_states[evaluator_name] = list(
                    set(self.essential_states) - set(achieved_essential_states)
                )
                self.logger.log(
                    logging.INFO,
                    f"Evaluator - {evaluator_name} - Achieved States: {self.achieved_essential_states[evaluator_name]}",
                )
                self.logger.log(
                    logging.INFO,
                    f"Evaluator - {evaluator_name} - Unachieved States: {self.unachieved_essential_states[evaluator_name]}",
                )

            self.history["achieved_essential_states"][
                f"{self.step-group_steps}-{self.step}"
            ] = eval_results

    def save_essential_states_eval_results(self, save_dir: Path) -> None:
        final_results = {
            "essential_states": self.essential_states,
            "achieved_essential_states": self.achieved_essential_states,
            "unachieved_essential_states": self.unachieved_essential_states,
        }

        with open(save_dir / "essential_states_dynamic_eval_result.json", "w") as f:
            json.dump(final_results, f, indent=2)
