import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Select 'learn' section tab in Coursera app.",
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
    parser = ETParser(history["xml"][-1])
    learn_element = parser.get_element_bydic(
        {
            "text": "Learn",
            "resource-id": "org.coursera.android:id/navigation_bar_item_large_label_view",
        }
    )

    if learn_element is None:
        return False

    if learn_element.attrib["selected"] == "false":
        return False

    return True
