import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser

# app-id : "GoogleTasks": "com.google.android.apps.tasks"


def task() -> str:
    return {
        "task": "Add a new list named 'Assignment' in Google Tasks.",
        "level": "easy",
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
    if len(history["xml"]) < 2:
        return False

    parser = ETParser(history["xml"][-1])

    list_selected_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/list_creation_tab"
    )

    if list_selected_element is None:
        return False

    if list_selected_element.attrib["content-desc"] != "Assignment":
        return False

    parser = ETParser(history["xml"][-2])

    create_bar_element = parser.get_element("text", "Create new list")

    if create_bar_element is None:
        return False

    done_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/done_button"
    )

    if done_element is None:
        return False

    done_button = parser.find_clickable_parent(done_element)

    # "[1,2][3,4]" -> [1,2,3,4]
    bounds_str = done_button.attrib["bounds"].replace("][", ",")

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
