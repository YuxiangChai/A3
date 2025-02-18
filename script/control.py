import argparse
import json
import logging
import time
from pathlib import Path

import yaml
from ace.utils.avd_control import Controller
from ace.utils.common_utils import check_create_dir, get_logger, print_results
from ace.utils.essential_states import GPTStateGen
from ace.utils.register import register_tasks, register_translator

if __name__ == "__main__":
    app_package = {
        "bluecoins": "com.rammigsoftware.bluecoins",
        "booking": "com.booking",
        "booking.com": "com.booking",
        "google calendar": "com.google.android.calendar",
        "calendar": "com.google.android.calendar",
        "cnn": "com.cnn.mobile.android.phone",
        "coursera": "org.coursera.android",
        "doordash": "com.dd.doordash",
        "fitbit": "com.fitbit.FitbitMobile",
        "gmail": "com.google.android.gm",
        "google maps": "com.google.android.apps.maps",
        "maps": "com.google.android.apps.maps",
        "google play": "com.android.vending",
        "google play store": "com.android.vending",
        "googleplaybooks": "com.google.android.apps.books",
        "google play books": "com.google.android.apps.books",
        "googletasks": "com.google.android.apps.tasks",
        "google tasks": "com.google.android.apps.tasks",
        "instagram": "com.instagram.android",
        "quora": "com.quora.android",
        "smart news": "jp.gocro.smartnews.android",
        "target": "com.target.ui",
        "wish": "com.contextlogic.wish",
        "yelp": "com.yelp.android",
        "youtube": "com.google.android.youtube/.app.honeycomb.Shell$HomeActivity",
        "ytmusic": "com.google.android.apps.youtube.music",
        "youtube music": "com.google.android.apps.youtube.music",
    }

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config/control_config.yaml",
        help="The config file path",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the demo test actions",
    )
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    translator = register_translator(
        f"avd_control/translator/{config['agent']['name']}.py", config
    )
    tasks, pre_tasks = register_tasks(config["tasks"])

    if config["continue_execution"]:
        existing_tasks = []
        last_task_idx = 0
        existing_tasks_dir = Path(config["save_dir"]) / config["eval_exp_name"]
        if existing_tasks_dir.exists():
            for dir in existing_tasks_dir.iterdir():
                if dir.is_dir():
                    try:
                        with open(
                            dir / "histories" / f"{dir.stem}_history.json", "r"
                        ) as f:
                            task_detail = json.load(f)
                            existing_tasks.append(task_detail[0]["task"])
                            last_task_idx = max(
                                int(dir.stem.split("_")[-1]), last_task_idx
                            )
                    except FileNotFoundError:
                        last_task_idx = max(int(dir.stem.split("_")[-1]), last_task_idx)
                        continue

        new_tasks = []
        for t in tasks:
            if t["task"] not in existing_tasks:
                new_tasks.append(t)

    # get all app package names
    app_ids = {}
    for t in tasks:
        if not t["app"].lower() in app_package:
            app_ids[t["app"].lower()] = t["app_package"]

    log_dir = check_create_dir(Path(config["log_dir"]))
    logger = get_logger(log_dir, f"{config['eval_exp_name']}")

    controller = Controller(
        config,
        app_ids=app_package,
        logger=logger,
        udid=config["udid"],
    )

    if config["eval_essential_state"]:
        group_steps = config["eval_essential_state_group_steps"]
        interval = config["eval_essential_state_interval"]

    save_dir = check_create_dir(Path(config["save_dir"]) / config["eval_exp_name"])

    results = []

    # demo_test_actions = [
    #     {"action": "tap", "x": 720, "y": 1400},
    #     {"action": "tap", "x": 570, "y": 400},
    #     {"action": "tap", "x": 650, "y": 600},
    #     {"action": "tap", "x": 650, "y": 800},
    #     {"action": "type", "text": "beijing"},
    #     {"action": "tap", "x": 650, "y": 800},
    #     {"action": "tap", "x": 650, "y": 1000},
    #     {"action": "type", "text": "shanghai"},
    #     {"action": "tap", "x": 650, "y": 800},
    #     {"action": "tap", "x": 650, "y": 1200},
    #     {"action": "tap", "x": 800, "y": 1200},
    #     {"action": "tap", "x": 800, "y": 2900},
    #     {"action": "tap", "x": 800, "y": 1400},
    #     {"action": "tap", "x": 1300, "y": 850},
    #     {"action": "tap", "x": 1000, "y": 2900},
    #     {"action": "tap", "x": 720, "y": 1600},
    #     {"action": "end"},
    # ]
    demo_test_actions = [
        {"action": "open", "app": "Settings"},
        {
            "action": "swipe",
            "x1": 720,
            "y1": 2800,
            "x2": 720,
            "y2": 400,
            "duration": 100,
        },
        {"action": "tap", "x": 720, "y": 2600},
        {"action": "tap", "x": 720, "y": 1300},
        {"action": "tap", "x": 720, "y": 800},
        {"action": "end"},
    ]

    controller._terminate_all_apps()
    time.sleep(1)

    # for pre_task in pre_tasks:
    #     pre_task(controller)

    for task_idx, t in enumerate(new_tasks):
        app = t["app"]
        app_package = t["app_package"]
        task = t["task"]
        # task_idx = t["task_idx"]
        category = t["category"]
        task_level = t["task_level"]

        new_task_idx = int(last_task_idx) + task_idx

        if task_level == "easy":
            max_steps = 10
        elif task_level == "medium":
            max_steps = 15
        elif task_level == "hard":
            max_steps = 20

        if config["eval_essential_state"]:
            if "essential_states" not in t and config["essential_states_generation"]:
                if config["essential_states_generation_name"] == "gpt":
                    state_generator = GPTStateGen(
                        config["essential_states_generation_sk"],
                        config["essential_states_generation_model"],
                    )
                    essential_states = state_generator.generate_states(task)
                    essential_states = json.loads(essential_states)
                    essential_states = essential_states["answer"]
            elif (
                "essential_states" not in t
                and not config["essential_states_generation"]
            ):
                raise ValueError(
                    "Essential states are not provided and essential states generation is disabled"
                )
            else:
                essential_states = t["essential_states"]

            essential_states = [s["state"] for s in essential_states]
        else:
            essential_states = []

        # create save directories
        if config["screen_record"]:
            record_save_dir = check_create_dir(
                save_dir / f"task_{new_task_idx}" / "record"
            )

        if config["state_save"]:
            state_save_dir = check_create_dir(
                save_dir / f"task_{new_task_idx}" / "states"
            )

        if config["history_save"]:
            history_save_dir = check_create_dir(
                save_dir / f"task_{new_task_idx}" / "histories"
            )

        if config["result_save"]:
            result_save_dir = check_create_dir(
                save_dir / f"task_{new_task_idx}" / "results"
            )

        controller.set_task_eval(
            task, new_task_idx, task_level, category, essential_states
        )
        controller._terminate_all_apps()
        time.sleep(1)
        controller.save_state(state_save_dir)

        if config["screen_record"]:
            controller.start_record(config["record_resolution"])

        while controller.step <= max_steps - 1:
            if controller.step == 0:
                logger.log(logging.INFO, f"Task {new_task_idx} Started - {task}")
            state = controller.get_state()
            history = controller.get_history()

            if not args.demo:
                # send state to the agent
                out_message = translator.to_agent(state, task, history)
                logger.log(logging.INFO, f"Agent Output: {out_message}")
                controller.save_history_agent_message(out_message)

                # translate the output to action
                action = translator.to_device(out_message, controller.w, controller.h)
            else:
                action = demo_test_actions[controller.step]
                controller.save_history_agent_message(repr(action))

            logger.log(logging.INFO, f"Action: {action}")

            # execute the action
            try:
                controller.exe_action(action)
            except Exception as e:
                action = {"action": "end", "answer": str(e)}
                controller.exe_action(action)

            # end the loop if the action is "end"
            if action["action"] == "end":
                if config["eval_essential_state"] and not config["only_execution"]:
                    controller.eval_essential_states()
                break

            # else wait for the device to fully respond (2 seconds)
            time.sleep(2)

            if controller.step <= max_steps - 1:
                controller.save_state(state_save_dir)

            if (
                config["eval_essential_state"]
                and not config["only_execution"]
                and (controller.step + 1 - group_steps) >= 0
                and (controller.step + 1 - group_steps) % interval == 0
            ):
                controller.eval_essential_states()

        if config["screen_record"]:
            controller.stop_save_record(record_save_dir)

        try:
            controller.save_history(history_save_dir)
        except Exception as e:
            logger.log(logging.ERROR, f"Error in saving history: {e}")
            history = controller.get_history()

        if not config["eval_essential_state"] and not config["only_execution"]:
            try:
                # evaluate the final state
                eval_result, eval_reasons = controller.eval_final_state()

                result = {
                    "task": task,
                    "task_idx": new_task_idx,
                    "app": app,
                    "app_package": app_package,
                    "essential_states": essential_states,
                    "result": eval_result,
                    "reasons": eval_reasons,
                }

                for key, value in eval_result.items():
                    print_result = (
                        "Task is successful"
                        if value.lower().strip(".") == "yes"
                        else "Task is failed"
                    )
                    logger.log(logging.INFO, f"{key} eval: {value}")

            except Exception as e:
                logger.log(
                    logging.ERROR, f"Error in evaluating task {new_task_idx}: {e}"
                )
                result = {
                    "task": task,
                    "task_idx": new_task_idx,
                    "app": app,
                    "app_package": app_package,
                    "essential_states": essential_states,
                    "result": "error",
                    "reasons": str(e),
                }

            results.append(result)

            with open(
                result_save_dir / f"final_state_dynamic_eval_result.json", "w"
            ) as f:
                json.dump(result, f, indent=2)

        elif not config["only_execution"]:
            controller.save_essential_states_eval_results(result_save_dir)
        elif config["only_execution"]:
            pass
