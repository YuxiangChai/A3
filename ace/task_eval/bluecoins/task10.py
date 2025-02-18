import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Clear the 'Trash' section in bluecoins app.",
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
    parser = ETParser(history["xml"][-1])

    empty_trash_button = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/menu_empty_trash"
    )

    if empty_trash_button is None:
        return False

    empty_trash_list = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/empty_trash_list"
    )

    if empty_trash_list is not None:
        return False

    return True
