from ace.utils.avd_control import Controller
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Delete the latest post on Instagram",
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

    # Delete post takes at least 2 steps
    if len(history["actions"]) < 2:
        return False

    # The second last step is tap delete button
    parser = ETParser(history["xml"][-3])
    element = parser.get_element_bydic(
        {
            "resource-id": "com.instagram.android:id/control_option_text",
            "text": "Delete",
        }
    )

    if element is None:
        return False

    if element.attrib["text"].lower() != "delete":
        return False

    # The last step is confirm deleting
    parser = ETParser(history["xml"][-2])
    element = parser.get_element(
        "resource-id", "com.instagram.android:id/igds_alert_dialog_primary_button"
    )

    if element is None:
        return False

    # "[1,2][3,4]" -> [1,2,3,4]
    bounds_str = element.attrib["bounds"].replace("][", ",")

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
