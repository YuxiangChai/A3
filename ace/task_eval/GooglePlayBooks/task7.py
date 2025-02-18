import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open wishlist in Google Play Books and sort items by price",
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
    wishlist_element = parser.get_element(
        "resource-id", "com.google.android.apps.books:id/bottom_wishlist"
    )
    if wishlist_element is None:
        return False

    if wishlist_element.attrib["selected"] != "true":
        return False

    wishlist_element_1 = parser.get_element_bydic(
        {"text": "Wishlist", "resource-id": ""}
    )

    if wishlist_element_1.attrib["selected"] != "true":
        return False

    sort_element = parser.get_element("content-desc", "Price, Sort filter")

    if sort_element is None:
        return False

    return True
