import glob
import xml.etree.ElementTree as ET

from ace.utils.avd_control import Controller
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Mark 'Python Assignment1' as completed in list 'Homework'.",
        "level": "medium",
        "category": "operation",
    }


def eval(
    task: str,
    xml: str,
    screenshot: str,  # base64 string of the current screenshot
    history: dict,  # history dictionary containing xml, screenshot and action
    answer: str = None,  # agent answer
    client=None,
    model_type: str = "gpt-4o-2024-11-20",
) -> bool:
    if (len(history["xml"])) < 2:
        return False

    # after adding task, the first task must be the new task
    parser = ETParser(history["xml"][-2])

    # check whether the list is correctly selected
    list_selected_element = parser.get_element_bydic(
        {
            "text": "Homework",
            "resource-id": "com.google.android.apps.tasks:id/task_list_title",
        }
    )

    if list_selected_element is None:
        return False

    # check if the task is correct
    task_element = parser.get_element_contains("content-desc", "Python Assignment1")

    if task_element is None:
        return False

    # find mark button
    mark_button = task_element.findall("*")[1]

    # "[1,2][3,4]" -> [1,2,3,4]
    bounds_str = mark_button.attrib["bounds"].replace("][", ",")

    # 1. 去掉方括号
    bounds_str = bounds_str.strip("[]")

    # 2. 将字符串按逗号分割
    bounds = list(map(int, bounds_str.split(",")))
    # if the last action is tap and it taps the right region
    if (
        history["actions"][-2]["action"] == "tap"
        and history["actions"][-2]["x"] > bounds[0]
        and history["actions"][-2]["x"] < bounds[2]
        and history["actions"][-2]["y"] > bounds[1]
        and history["actions"][-2]["y"] < bounds[3]
    ):
        return True
    else:
        return False
