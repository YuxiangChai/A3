import base64
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import easyocr
from ace.evaluators import *
from ace.utils.common_utils import combine_screenshots, parse_xmls
from ace.utils.som import draw_mark


class StaticOneTaskEvaluator:
    def __init__(self, config: dict, data_dir: Path) -> None:
        self.config = config
        self.data_dir = data_dir
        self.screenshots_dir = self.data_dir / "states" / "screenshots"
        self.xmls_dir = self.data_dir / "states" / "xmls"
        self.reader = easyocr.Reader(["ch_sim", "en"])

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
            if "base_url" in evaluator:
                state_eval = GPTStateEval(
                    sk=sk, model=model, base_url=evaluator["base_url"]
                )
            else:
                state_eval = GPTStateEval(sk=sk, model=model)
        elif evaluator["name"] == "gemini":
            if "base_url" in evaluator:
                state_eval = GeminiStateEval(
                    sk=sk, model=model, base_url=evaluator["base_url"]
                )
            else:
                state_eval = GeminiStateEval(sk=sk, model=model)
        elif evaluator["name"] == "claude":
            if "base_url" in evaluator:
                state_eval = ClaudeStateEval(
                    sk=sk, model=model, base_url=evaluator["base_url"]
                )
            else:
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

    def evaluate_one_state(
        self,
        eval_results: dict,
        screenshots: list,
        xmls: list,
        states: list,
        step: int,
        group_steps: int,
    ) -> dict:

        screenshot = []
        for s in screenshots:
            with open(s, "rb") as f:
                screenshot.append(f.read())
        xml = []
        for x in xmls:
            with open(x, "r") as f:
                xml.append(f.read())

        combined_screenshot = combine_screenshots(screenshot)

        if self.config["eval_modality_text"] == "xml":
            elements = parse_xmls(xml)
        elif self.config["eval_modality_text"] == "ocr":
            elements = []
            for s in screenshot:
                elements.append(self._ocr(s))
        else:
            raise ValueError(
                f"Unknown text modality: {self.config['eval_modality_text']}"
            )

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_evaluator = {
                executor.submit(
                    self.evaluate_state_worker,
                    evaluator,
                    elements,
                    combined_screenshot,
                    states,
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
                        "step": f"{step}-{step+group_steps}",
                        "achieved_essential_states": achieved_essential_states,
                        "answer": answer,
                        "reason": reason,
                    }
                )

        return eval_results

    def evaluate_essential_states(self, states: list[str]) -> list[dict]:
        group_steps = self.config["eval_essential_state_group_steps"]

        all_screenshots = sorted(
            self.screenshots_dir.glob("*.png"),
            key=lambda x: int(
                x.stem.split("_")[-1],
            ),
        )
        all_xmls = sorted(
            self.xmls_dir.glob("*.xml"),
            key=lambda x: int(
                x.stem.split("_")[-1],
            ),
        )

        step = 0
        eval_results = {}

        if len(all_screenshots) < group_steps:
            eval_results = self.evaluate_one_state(
                eval_results,
                all_screenshots,
                all_xmls,
                states,
                step,
                len(all_screenshots) - 1,
            )
        else:
            while step <= len(all_screenshots) - group_steps:
                screenshots = all_screenshots[step : step + group_steps]
                xmls = all_xmls[step : step + group_steps]

                eval_results = self.evaluate_one_state(
                    eval_results, screenshots, xmls, states, step, group_steps
                )

                # cv2.imwrite(
                #     f"combined_{step}.png",
                #     cv2.imdecode(
                #         np.frombuffer(combined_screenshot, np.uint8), cv2.IMREAD_COLOR
                #     ),
                # )

                if step == len(all_screenshots) - group_steps:
                    break

                step += self.config["eval_essential_state_interval"]
                if step > len(all_screenshots) - group_steps:
                    step = len(all_screenshots) - group_steps

        with open(
            self.data_dir / "results" / "essential_states_raw_static_eval_results.json",
            "w",
        ) as f:
            json.dump(eval_results, f, indent=2)

        return eval_results

    def evaluate_final_state_worker(
        self,
        task: str,
        evaluator: dict,
        elements: list[dict],
        screenshot: bytes,
    ) -> tuple[dict, dict]:
        sk = evaluator["sk"]
        model = evaluator["model"]

        if evaluator["name"] == "gpt":
            state_eval = GPTEvaluator(sk=sk, model=model)
        elif evaluator["name"] == "gemini":
            state_eval = GeminiEvaluator(sk=sk, model=model)
        elif evaluator["name"] == "claude":
            state_eval = ClaudeEvaluator(sk=sk, model=model)
        else:
            raise ValueError(f"Unknown evaluator: {evaluator['name']}")

        response_result = state_eval.eval(
            task,
            elements,
            screenshot,
        )

        return evaluator["name"], response_result

    def evaluate_final_state(self, task: str) -> None:
        all_screenshots = sorted(
            self.screenshots_dir.glob("*.png"),
            key=lambda x: int(
                x.stem.split("_")[-1],
            ),
        )
        all_xmls = sorted(
            self.xmls_dir.glob("*.xml"),
            key=lambda x: int(
                x.stem.split("_")[-1],
            ),
        )

        final_screenshot = all_screenshots[-1]
        final_xml = all_xmls[-1]

        with open(final_screenshot, "rb") as f:
            final_screenshot = f.read()

        with open(final_xml, "r") as f:
            final_xml = f.read()

        if self.config["eval_modality_text"] == "xml":
            elements = parse_xmls([final_xml])[0]
        elif self.config["eval_modality_text"] == "ocr":
            elements = self._ocr(final_screenshot)
        else:
            raise ValueError(
                f"Unknown text modality: {self.config['eval_modality_text']}"
            )

        if self.config["eval_screenshot_som"]:
            final_screenshot = draw_mark(base64.b64encode(final_screenshot), elements)

        # Run evaluators in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_evaluator = {
                executor.submit(
                    self.evaluate_final_state_worker,
                    task,
                    evaluator,
                    elements,
                    final_screenshot,
                ): evaluator
                for evaluator in self.config["evaluators"]
            }

            results = {}
            reasons = {}
            for future in as_completed(future_to_evaluator):
                evaluator_name, response_result = future.result()
                try:
                    response_result = json.loads(response_result)
                    answer = response_result["answer"]
                    reason = response_result["reason"]
                except json.JSONDecodeError:
                    answer = None
                    reason = response_result

                results[evaluator_name] = answer
                reasons[evaluator_name] = reason

        final_result = {
            "results": results,
            "reasons": reasons,
        }

        return final_result
