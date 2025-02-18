import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Write a new post 'Good morning' in Quora.",
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

    post_element = parser.get_element_contains_from(
        "text", "Good morning", "resource-id", "com.quora.android:id/backButton"
    )

    if post_element is None:
        return False

    return True
