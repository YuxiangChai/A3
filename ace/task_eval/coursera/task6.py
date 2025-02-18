import glob
import xml.etree.ElementTree as ET

from ace.utils.avd_control import Controller
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open course 'cryptography' under 'learn' section tab in coursera app.",
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
    course_name_element = parser.get_element(
        "resource-id", "org.coursera.android:id/courseName"
    )

    if course_name_element is None:
        return False

    if course_name_element.attrib["text"].lower().find("cryptography") == -1:
        return False

    return True
