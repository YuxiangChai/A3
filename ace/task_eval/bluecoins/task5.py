import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search 'food' in 'transactions' section in the bluecoins app.",
        "level": "middle",
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

    transaction_element = parser.get_element("content-desc", "Transactions")

    if transaction_element is None:
        return False

    if transaction_element.attrib["selected"] != "true":
        return False

    src_text_element = parser.get_element(
        "resource-id", "com.rammigsoftware.bluecoins:id/search_src_text"
    )

    if src_text_element is None:
        return False

    if src_text_element.attrib["text"].lower() != "food":
        return False

    return True
