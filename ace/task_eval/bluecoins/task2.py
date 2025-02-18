import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In bluecoins, how much is the net earning on Dec 9, 2024",
        "level": "hard",
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
    month_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/month_name"
    )

    if month_element is None:
        return False

    # if not dec 2024
    if month_element.attrib["text"] != "December 2024":
        return False

    date_element = parser.get_element_contains_from(
        "content-desc", "9", "content-desc", "Calendar"
    )

    # if not dec 9
    if date_element.attrib["checked"] == "false":
        return False

    no_transaction_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/empty_tab"
    )

    if no_transaction_element is not None:
        gt = "0.00"
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    net_earning_element = parser.get_element_contains_from(
        "resource-id",
        "com.rammigsoftware.bluecoins:id/amount_tv",
        "text",
        "NET EARNINGS",
    )

    if net_earning_element is None:
        gt = "0.00"
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    gt = net_earning_element.attrib["text"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
