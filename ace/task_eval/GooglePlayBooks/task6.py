import glob
import xml.etree.ElementTree as ET

from ace.utils.avd_control import Controller
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Remove Hemingway's 'In Our Time' from my wishlist in Google Play Books.",
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
    if len(history["xml"]) < 2:
        return False
    parser = ETParser(history["xml"][-2])

    # check if it is in single-stream page
    tools_element = parser.get_element(
        "resource-id", "com.google.android.apps.books:id/closed_toolbar_title"
    )

    if tools_element is None:
        remove_element = parser.get_element_contains_from_contains(
            "content-desc", "Remove from wishlist", "content-desc", "Romeo And Juliet"
        )

        if remove_element is None:
            return False

    else:
        book_element = parser.get_element_contains("content-desc", "In Our Time")

        if book_element is None:
            return False

        remove_element = parser.get_element("content-desc", "Remove from wishlist")

        if remove_element is None:
            return False

    remove_button = parser.find_clickable_parent(remove_element)

    # "[1,2][3,4]" -> [1,2,3,4]
    bounds_str = remove_button.attrib["bounds"].replace("][", ",")

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
