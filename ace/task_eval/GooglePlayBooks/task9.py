import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open Google play books and tell me what is the top selling book now, who is the author, what is its overall rating and how much is it.",
        "level": "medium",
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

    top_selling_element = parser.get_element("text", "Top charts")

    if top_selling_element is None:
        return False

    book_element = parser.get_element(
        "resource-id",
        "com.google.android.apps.books:id/card_image_body_button_list_item_root",
    )

    if book_element is None:
        return False

    gt = book_element.attrib["content-desc"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
