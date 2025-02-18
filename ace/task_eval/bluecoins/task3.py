import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Record a 'food' expenditure of $100 on Dec 9, 2024 in bluecoins app.",
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
    parser = ETParser(history["xml"][-2])
    date_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/date_edittext"
    )

    if date_element is None:
        return False

    if date_element.attrib["text"] != "December 9, 2024":
        return False

    name_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/item_autocomplete_textview"
    )

    if name_element is None:
        return False

    if name_element.attrib["text"].lower() != "food":
        return False

    sign_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/amount_sign_textview"
    )

    if sign_element is None:
        return False

    if sign_element.attrib["text"] != "-":
        return False

    amount_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/amount_tv"
    )

    if amount_element is None:
        return False

    if amount_element.attrib["text"] != "100":
        return False

    save_button = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/fab"
    )

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
