import argparse
import json
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target_dir",
        "-d",
        type=str,
        default="../AVD-Control-Evaluation/save_dir/ui-tars-7b-sft/",
        help="Path to the folder containing evaluation results",
    )
    args = parser.parse_args()

    eval_dir = Path(args.target_dir)
    eval_overall = {
        "success": 0,
        "fail": 0,
    }
    eval_results_by_level = {
        "easy": {"success": 0, "fail": 0},
        "medium": {"success": 0, "fail": 0},
        "hard": {"success": 0, "fail": 0},
    }
    eval_results_by_category = {
        "operation": {"success": 0, "fail": 0},
        "single-page query": {"success": 0, "fail": 0},
        "multi-page query": {"success": 0, "fail": 0},
    }
    for task_dir in eval_dir.iterdir():
        if not task_dir.is_dir():
            continue
        task_idx = int(task_dir.stem.split("_")[-1])

        try:
            with open(task_dir / "results" / "func_eval_results.json", "r") as f:
                task_result = json.load(f)
        except FileNotFoundError:
            continue

        task_level = task_result["task_level"]
        task_level = "medium" if task_level == "middle" else task_level
        category = task_result["category"]
        category = (
            "single-page query" if category == "single-page operation" else category
        )

        if task_result["eval_results"]:
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
            f"{level}: {results['success']} success, {results['fail']} fail, success rate: {results['success'] / (results['success'] + results['fail'])}"
        )

    print("Evaluation results by category:")
    for category, results in eval_results_by_category.items():
        print(
            f"{category}: {results['success']} success, {results['fail']} fail, success rate: {results['success'] / (results['success'] + results['fail'])}"
        )

    print("Overall evaluation results:")
    print(
        f"{eval_overall['success']} success, {eval_overall['fail']} fail, success rate: {eval_overall['success'] / (eval_overall['success'] + eval_overall['fail'])}"
    )
