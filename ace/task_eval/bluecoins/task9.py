import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "What is the most recently deleted transaction in the bluecoins app?",
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
    empty_trash_button = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/menu_empty_trash"
    )

    if empty_trash_button is None:
        return False

    item_list_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/recyclerview"
    )

    if item_list_element is None:
        gt = "There is no transaction in the 'Trash'."
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    item_name_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/item_tv"
    )

    item_amount_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/amount_tv"
    )

    item_category_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/category_tv"
    )

    item_account_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/account_tv"
    )

    item_date_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/date_tv"
    )

    gt = f"name: {item_name_element.attrib['text']}, amount: {item_amount_element.attrib['text']}, category: {item_category_element.attrib['text']}, account: {item_account_element.attrib['text']}, date: {item_date_element.attrib['text']}"

    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
