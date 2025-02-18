import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open 'Downloads' section tab in coursera.",
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

    title_element = parser.get_element(
        "resource-id", "org.coursera.android:id/toolbar_title"
    )

    if title_element is None:
        return False

    if title_element.attrib["text"] != "Downloads":
        return False

    return True
