import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Sort my 'Homework' list by date in google tasks.",
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

    # click sort button
    parser = ETParser(history["xml"][-2])

    sort_element = parser.get_element_bydic(
        {"text": "Sort by", "resource-id": "com.google.android.apps.tasks:id/title"}
    )

    if sort_element is None:
        return False

    sort_date_element = parser.get_element_bydic(
        {
            "text": "Date",
            "resource-id": "com.google.android.apps.tasks:id/task_list_menu_item_text",
        }
    )

    sort_date_button = parser.find_clickable_parent(sort_date_element)

    # "[1,2][3,4]" -> [1,2,3,4]
    bounds_str = sort_date_button.attrib["bounds"].replace("][", ",")

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
