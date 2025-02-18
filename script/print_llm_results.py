import argparse
import json
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target_dir",
        "-d",
        type=str,
        default="save_dir/qwen2.5-vl-7b/",
        help="Path to the folder containing evaluation results",
    )
    args = parser.parse_args()

    eval_dir = Path(args.target_dir)
    eval_overall = {
        "success": 0,
        "fail": 0,
        "essential": {"success": 0, "fail": 0},
    }
    eval_results_by_level = {
        "easy": {"success": 0, "fail": 0, "essential": {"success": 0, "fail": 0}},
        "medium": {"success": 0, "fail": 0, "essential": {"success": 0, "fail": 0}},
        "hard": {"success": 0, "fail": 0, "essential": {"success": 0, "fail": 0}},
    }
    eval_results_by_category = {
        "operation": {"success": 0, "fail": 0, "essential": {"success": 0, "fail": 0}},
        "single-page query": {
            "success": 0,
            "fail": 0,
            "essential": {"success": 0, "fail": 0},
        },
        "multi-page query": {
            "success": 0,
            "fail": 0,
            "essential": {"success": 0, "fail": 0},
        },
    }
    for task_dir in eval_dir.iterdir():
        if not task_dir.is_dir():
            continue
        task_idx = int(task_dir.stem.split("_")[-1])

        try:
            with open(
                task_dir / "results" / "essential_states_static_eval_results.json", "r"
            ) as f:
                task_result = json.load(f)
        except FileNotFoundError:
            continue

        task_level = task_result["task_level"]
        task_level = "medium" if task_level == "middle" else task_level
        category = task_result["category"]
        category = (
            "single-page query" if category == "single-page operation" else category
        )

        all_essential_states = task_result["essential_states"]
        achieved_states = []
        for name, states in task_result["achieved_essential_states"].items():
            achieved_states.extend(states)
        states_count = {
            state: achieved_states.count(state) for state in all_essential_states
        }

        for state, count in states_count.items():
            if count >= 2:
                eval_results_by_level[task_level]["essential"]["success"] += 1
                eval_results_by_category[category]["essential"]["success"] += 1
                eval_overall["essential"]["success"] += 1
            else:
                eval_results_by_level[task_level]["essential"]["fail"] += 1
                eval_results_by_category[category]["essential"]["fail"] += 1
                eval_overall["essential"]["fail"] += 1

        results = task_result["eval_results"]
        success_count = sum(1 for result in results.values() if result == "success")
        total_count = len(results)
        success_rate = success_count / total_count
        if success_rate > 0.5:
            eval_results_by_level[task_level]["success"] += 1
            eval_results_by_category[category]["success"] += 1
            eval_overall["success"] += 1
        else:
            eval_results_by_level[task_level]["fail"] += 1
            eval_results_by_category[category]["fail"] += 1
            eval_overall["fail"] += 1

    print("Evaluation results by level:")
    for level, results in eval_results_by_level.items():
        print(
            f"{level}: {results['success']} success, {results['fail']} fail, success rate: {results['success'] / (results['success'] + results['fail'])}, essential success rate: {results['essential']['success'] / (results['essential']['success'] + results['essential']['fail'])}"
        )

    print("Evaluation results by category:")
    for category, results in eval_results_by_category.items():
        print(
            f"{category}: {results['success']} success, {results['fail']} fail, success rate: {results['success'] / (results['success'] + results['fail'])}, essential success rate: {results['essential']['success'] / (results['essential']['success'] + results['essential']['fail'])}"
        )

    print("Overall evaluation results:")
    print(
        f"{eval_overall['success']} success, {eval_overall['fail']} fail, success rate: {eval_overall['success'] / (eval_overall['success'] + eval_overall['fail'])}, essential success rate: {eval_overall['essential']['success'] / (eval_overall['essential']['success'] + eval_overall['essential']['fail'])}"
    )
