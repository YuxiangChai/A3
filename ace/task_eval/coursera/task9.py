import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open 'settings' in Coursera and switch to dark mode.",
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

    settings_element = parser.get_element_contains_from(
        "text", "Settings", "content-desc", "Back"
    )

    if settings_element is None:
        return False

    dark_mode_element = parser.get_element("text", "Dark Mode")

    if dark_mode_element is None:
        return False

    dark_mode_parent = parser.find_parent(dark_mode_element)

    if dark_mode_parent is None:
        return False

    if len(dark_mode_parent.findall("*")) == 1:
        return False

    return True
