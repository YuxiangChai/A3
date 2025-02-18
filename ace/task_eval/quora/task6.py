import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search for 'Artificial Intelligence' in Quora. And set filter to show topics only.",
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
    parser = ETParser(history["xml"][-1])

    follow_button_element = parser.get_element_contains_from(
        "class", "android.widget.ToggleButton", "text", "Artificial Intelligence"
    )

    if follow_button_element is None:
        return False

    if follow_button_element.attrib["text"].find("Following") == -1:
        return False

    return True
