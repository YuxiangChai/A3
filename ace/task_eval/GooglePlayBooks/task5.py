import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Add ebook 'Romeo and Juliet' to my wishlist in Google Play Books.",
        "level": "hard",
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

    book_element = parser.get_element_contains("text", "Romeo And Juliet")

    if book_element is None:
        return False

    format_element = parser.get_element("content-desc", "Ebook format")

    if format_element is None:
        return False

    remove_wishlist_element = parser.get_element("content-desc", "Remove from wishlist")

    if remove_wishlist_element is None:
        return False

    return True
