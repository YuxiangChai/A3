import glob
import xml.etree.ElementTree as ET

from ace.utils.avd_control import Controller
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open google tasks and add a task named 'Machine Learning Assignment1' at Tomorrow 11:59pm in the list 'Homework'",
        "level": "hard",
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
    # after adding task, the first task must be the new task
    parser = ETParser(history["xml"][-1])

    # check whether the list is correctly selected
    list_selected_element = parser.get_element_bydic(
        {
            "text": "Homework",
            "resource-id": "com.google.android.apps.tasks:id/task_list_title",
        }
    )

    if list_selected_element is None:
        return False

    # check whether all the info is correct
    task_info_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/task_data"
    )

    if task_info_element is None:
        return False

    task_info_list = task_info_element.findall("*")

    if task_info_list[0].attrib["text"] != "Machine Learning Assignment1":
        return False

    if task_info_list[1].attrib["text"] != "Tomorrow, 11:59 PM":
        return False

    # make sure creating new task is true. avoiding misjudge when list already exists the identical task
    parser = ETParser(history["xml"][-2])

    save_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/add_task_done"
    )

    if save_element is None:
        return False

    save_button = parser.find_clickable_parent(save_element)

    # "[1,2][3,4]" -> [1,2,3,4]
    bounds_str = save_button.attrib["bounds"].replace("][", ",")

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
