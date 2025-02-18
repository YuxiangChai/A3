import importlib
import json
from pathlib import Path

if __name__ == "__main__":
    task_root_dir = Path("a3/task_eval")
    tasks = []
    for task_dir in task_root_dir.iterdir():
        if task_dir.is_dir():
            task_dir = Path(task_dir)
            for task_file in task_dir.glob("*.py"):
                task_module = f"a3.task_eval.{task_dir.name}.{task_file.stem}"
                module = importlib.import_module(task_module)
                if hasattr(module, "task"):
                    task_dict = module.task()
                    print(task_dict)
                    print(type(task_dict))
                    task = task_dict["task"]
                    task_level = task_dict["level"]
                    category = task_dict["category"]
                    tasks.append(
                        {
                            "task_idx": len(tasks) + 1,
                            "task": task,
                        }
                    )
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)
