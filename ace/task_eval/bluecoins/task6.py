import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open 'budget summary' in the bluecoins app",
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
    bgt_element = parser.get_element_contains_from_until(
        "text",
        "Budget Summary",
        "class",
        "android.widget.ImageButton",
        "resource-id",
        "com.rammigsoftware.bluecoins:id/menu_filter",
    )

    if bgt_element is None:
        return False

    chart_element = parser.get_element("text", "Chart")

    if chart_element is None:
        return False

    return True
