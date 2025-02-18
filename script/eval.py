import argparse
import json
import logging
from pathlib import Path

import yaml
from ace.evaluators.static_evaluator import StaticOneTaskEvaluator
from ace.utils.common_utils import check_create_dir, get_logger
from ace.utils.essential_states import GPTStateGen
from ace.utils.register import register_tasks
from openai import OpenAI

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config/eval_config.yaml",
        help="The config file path",
    )
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    log_dir = check_create_dir(Path(config["log_dir"]))
    logger = get_logger(log_dir, "Evaluator")

    if config["eval_type"] == "function":
        tasks, _ = register_tasks("ace/task_eval")
        client = OpenAI(
            api_key=config["answer_judge"]["sk"],
            base_url="https://aihubmix.com/v1",
        )

    eval_dir = Path(config["eval_dir"])
    # task_count = 0
    for task_dir in eval_dir.iterdir():
        if config["eval_type"] == "llm":
            if (
                config["eval_essential_state"]
                and (
                    task_dir / "results" / "essential_states_static_eval_results.json"
                ).exists()
            ):
                continue
            if (
                not config["eval_essential_state"]
                and (
                    task_dir / "results" / "final_state_static_eval_results.json"
                ).exists()
            ):
                continue
            result_save_dir = check_create_dir(task_dir / "results")
            e = StaticOneTaskEvaluator(config, task_dir)
            task_idx = int(task_dir.stem.split("_")[-1])

            with open(
                task_dir / "histories" / f"task_{task_idx}_history.json", "r"
            ) as f:
                task_histories = json.load(f)

            task_dict = {
                "task": task_histories[0]["task"],
                "task_level": task_histories[0]["task_level"],
                "category": task_histories[0]["category"],
            }

            logger.log(
                logging.INFO,
                f"Start evaluating task {task_idx}:\n\t{task_dict['task']}\n",
            )

            if config["eval_essential_state"]:
                if (
                    "essential_states" not in task_dict
                    and config["essential_states_generation"]
                ):
                    if config["essential_states_generation_name"] == "gpt":
                        state_generator = GPTStateGen(
                            config["essential_states_generation_sk"],
                            config["essential_states_generation_model"],
                        )
                        essential_states = state_generator.generate_states(
                            task_dict["task"]
                        )
                        essential_states = json.loads(essential_states)
                        essential_states = essential_states["answer"]
                elif (
                    "essential_states" not in task_dict
                    and not config["essential_states_generation"]
                ):
                    raise ValueError(
                        "Essential states are not provided and essential states generation is disabled"
                    )
                else:
                    essential_states = task_dict["essential_states"]

                all_essential_states = [s["state"] for s in essential_states]

                eval_results = e.evaluate_essential_states(all_essential_states)

                # get all achieved essential states
                achieved_essential_states = {}
                unachieved_essential_states = {}
                final_eval_llms = {}
                for name, results in eval_results.items():
                    achieved_essential_states_dup = []
                    for res in results:
                        achieved_essential_states_dup.extend(
                            res["achieved_essential_states"]
                        )
                    achieved_essential_states[name] = list(
                        set(achieved_essential_states_dup)
                    )
                    unachieved_essential_states[name] = list(
                        set(all_essential_states) - set(achieved_essential_states[name])
                    )

                    # check if all essential states are achieved
                    if set(all_essential_states).issubset(
                        set(achieved_essential_states[name])
                    ):
                        logger.log(
                            logging.INFO, f"Evaluator {name} - Task is successful."
                        )
                        final_eval_llms[name] = "success"
                    else:
                        logger.log(logging.INFO, f"Evaluator {name} - Task is failed.")
                        logger.log(
                            logging.INFO,
                            f"Achieved essential states: {achieved_essential_states[name]}",
                        )
                        logger.log(
                            logging.INFO,
                            f"Unachieved essential states: {unachieved_essential_states[name]}\n",
                        )
                        final_eval_llms[name] = "fail"

                final_results = {
                    "task": task_dict["task"],
                    "task_level": task_dict["task_level"],
                    "category": task_dict["category"],
                    "eval_results": final_eval_llms,
                    "essential_states": all_essential_states,
                    "achieved_essential_states": achieved_essential_states,
                    "unachieved_essential_states": unachieved_essential_states,
                }

                with open(
                    result_save_dir / "essential_states_static_eval_results.json", "w"
                ) as f:
                    json.dump(final_results, f, indent=2)
            else:
                eval_results = e.evaluate_final_state(task_dict["task"])

                final_results = {
                    "task": task_dict["task"],
                    "task_level": task_dict["task_level"],
                    "category": task_dict["category"],
                    "eval_results": eval_results["results"],
                    "reasons": eval_results["reasons"],
                }

                with open(
                    result_save_dir / "final_state_static_eval_results.json", "w"
                ) as f:
                    json.dump(final_results, f, indent=2)

        elif config["eval_type"] == "function":
            result_save_dir = check_create_dir(task_dir / "results")
            task_idx = int(task_dir.stem.split("_")[-1])
            with open(
                task_dir / "histories" / f"task_{task_idx}_history.json", "r"
            ) as f:
                task_histories = json.load(f)

            task_dict = {
                "task": task_histories[0]["task"],
                "task_level": task_histories[0]["task_level"],
                "category": task_histories[0]["category"],
            }

            for task in tasks:
                if task["task"] == task_dict["task"]:
                    eval_func = task["eval"]
                    break

            xmls = []
            screenshots = []
            histories = {
                "actions": [],
            }

            for history in task_histories:
                with open(task_dir / "states" / "xmls" / history["xml"], "r") as f:
                    xmls.append(f.read())
                with open(
                    task_dir / "states" / "screenshots" / history["screenshot"], "rb"
                ) as f:
                    screenshots.append(f.read())

                histories["actions"].append(history["actions"])
                if history["actions"]["action"] == "end":
                    answer = history["actions"]["answer"]

            histories["xml"] = xmls
            histories["screenshot"] = screenshots

            try:
                eval_result = eval_func(
                    task_dict["task"],
                    xmls[-1],
                    screenshots[-1],
                    histories,
                    answer,
                    client,
                    config["answer_judge"]["model"],
                )
            except Exception as e:
                logger.log(
                    logging.ERROR,
                    f"Error occurred while evaluating task {task_idx}:\n{e}",
                )
                eval_result = False

            result_save_dir = check_create_dir(task_dir / "results")
            with open(result_save_dir / "func_eval_results.json", "w") as f:
                json.dump(
                    {
                        "task": task_dict["task"],
                        "task_level": task_dict["task_level"],
                        "category": task_dict["category"],
                        "eval_results": eval_result,
                    },
                    f,
                    indent=2,
                )
