import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "On the Quora space page, select all spaces I might like.",
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

    suggested_spaces_element = parser.get_element("text", "Suggested Spaces to Follow")

    if suggested_spaces_element is None:
        return False

    return True
