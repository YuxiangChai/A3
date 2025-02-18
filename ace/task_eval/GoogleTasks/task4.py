import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Sort my 'Homework' list by date in Google tasks, and then star the most urgent task.",
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

    parser = ETParser(history["xml"][-2])

    # check if it is Homework list
    list_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/task_list_title"
    )

    if list_element is None:
        return False

    if list_element.attrib["text"] != "Homework":
        return False

    # no task
    no_task_element = parser.get_element("text", "No tasks yet")

    if no_task_element is not None:
        return True

    # all task completed
    all_task_complete_element = parser.get_element("text", "All tasks completed")

    if all_task_complete_element is not None:
        return True

    task_list_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/tasks_list"
    )

    # if it didn't sort
    if task_list_element.findall("*")[1].attrib["class"] != "android.widget.TextView":
        return False

    # sort wrongly
    if (
        task_list_element.findall("*")[1].attrib["text"] == "Starred recently"
        or task_list_element.findall("*")[1].attrib["text"] == "Not starred"
    ):
        return False

    star_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/star_button"
    )

    if star_element is None:
        return False

    # if it is already starred, do nothing, return true
    if star_element.attrib["content-desc"] == "Remove star":
        return True

    star_button = parser.find_clickable_parent(star_element)

    # "[1,2][3,4]" -> [1,2,3,4]
    bounds_str = star_button.attrib["bounds"].replace("][", ",")

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
