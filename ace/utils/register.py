import importlib
import json
from pathlib import Path

from ace.translator.base import BaseTranslator

app_package = {
    "bluecoins": "com.rammigsoftware.bluecoins",
    "booking": "com.booking",
    "google_calendar": "com.google.android.calendar",
    "CNN": "com.cnn.mobile.android.phone",
    "coursera": "org.coursera.android",
    "doordash": "com.dd.doordash",
    "fitbit": "com.fitbit.FitbitMobile",
    "Gmail": "com.google.android.gm",
    "google_maps": "com.google.android.apps.maps",
    "google_play": "com.android.vending",
    "GooglePlayBooks": "com.google.android.apps.books",
    "GoogleTasks": "com.google.android.apps.tasks",
    "instagram": "com.instagram.android",
    "quora": "com.quora.android",
    "smart_news": "jp.gocro.smartnews.android",
    "target": "com.target.ui",
    "wish": "com.contextlogic.wish",
    "yelp": "com.yelp.android",
    "youtube": "com.google.android.youtube",
    "YTmusic": "com.google.android.apps.youtube.music",
}


def register_translator(translator_file: Path | str, config: dict) -> BaseTranslator:
    """get the translator object from the translator file

    Args:
        translator_file (Path | str): the path to the translator file

    Raises:
        AttributeError: The translator file does not have register method

    Returns:
        BaseTranslator: The translator object
    """
    if isinstance(translator_file, str):
        translator_file = Path(translator_file)

    translator_module = f"ace.translator.{translator_file.stem}"
    module = importlib.import_module(translator_module)
    if hasattr(module, "register"):
        cls = module.register(config)
        return cls
    else:
        raise AttributeError(
            f"translator {translator_file.stem} does not have register method"
        )


def register_tasks(tasks: Path | str) -> list[dict]:
    """get the tasks

    Args:
        task_dir (Path | str): The path to tasks

    Returns:
        list[dict]: a list contains dictionaries containing the `task` and `eval` function
    """
    if isinstance(tasks, Path):
        tasks = tasks.as_posix()

    if tasks.endswith(".json"):
        with open(tasks, "r") as f:
            ret_tasks = json.load(f)
    else:
        ret_tasks = []
        pre_tasks = []
        task_dir = Path(tasks)
        for app_folder in task_dir.iterdir():
            app_name = app_folder.name
            if app_folder.is_dir():
                for task_file in app_folder.glob("*.py"):
                    task_module = f"ace.task_eval.{app_name}.{task_file.stem}"
                    module = importlib.import_module(task_module)
                    if hasattr(module, "pre_task"):
                        pre_task = module.pre_task
                        pre_tasks.append(pre_task)
                        continue
                    if hasattr(module, "task"):
                        task_dict = module.task()
                        task = task_dict["task"]
                        task_level = task_dict["level"]
                        category = task_dict["category"]
                        eval = module.eval
                        ret_tasks.append(
                            {
                                "app": app_name,
                                "app_package": app_package[app_name],
                                "task": task,
                                "eval": eval,
                                "task_level": task_level,
                                "category": category,
                            }
                        )

    return ret_tasks, None if not pre_tasks else pre_tasks
