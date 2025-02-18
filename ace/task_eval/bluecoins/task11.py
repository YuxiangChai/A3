import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Find settings in bluecoins app.",
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

    tool_bar_top_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/toolbar_top"
    )

    if tool_bar_top_element is None:
        return False

    setting_element = tool_bar_top_element.findall("*")[1]

    if setting_element.attrib["text"] != "Settings":
        return False

    return True
