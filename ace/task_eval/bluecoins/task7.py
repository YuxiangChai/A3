import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In the bluecoins app, open 'budget summary' and tell me how much budget left for this month.",
        "level": "easy",
        "category": "single-page query",
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

    remaining_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/remaining_amount_textview"
    )

    if remaining_element is None:
        return False

    gt = remaining_element.attrib["text"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
