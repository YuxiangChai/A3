import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Is 'Journey to the West' in my google play books' wishlist?",
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

    in_wishlist = False
    gt = ""
    find_gt = False
    for xml in history["xml"]:
        parser = ETParser(xml)
        if not in_wishlist:
            wishlist_element = parser.get_element(
                "resource-id", "com.google.android.apps.books:id/bottom_wishlist"
            )

            if wishlist_element is None:
                continue

            if wishlist_element.attrib["selected"] != "true":
                continue

            wishlist_element_1 = parser.get_element_bydic(
                {"text": "Wishlist", "resource-id": ""}
            )

            if wishlist_element_1 is None:
                continue

            if wishlist_element_1.attrib["selected"] != "true":
                continue

            in_wishlist = True

        else:

            wishlist_element = parser.get_element(
                "resource-id", "com.google.android.apps.books:id/bottom_wishlist"
            )

            if wishlist_element is None:
                continue

            if wishlist_element.attrib["selected"] != "true":
                in_wishlist = False
                continue

            wishlist_element_1 = parser.get_element_bydic(
                {"text": "Wishlist", "resource-id": ""}
            )

            if (
                wishlist_element_1 is not None
                and wishlist_element_1.attrib["selected"] != "true"
            ):
                in_wishlist = False
                continue

            book_element = parser.get_element_contains("text", "Journey to the West")

            if book_element is None:
                continue

            gt = "Yes, Journey to the West is in your wishlist"

    if in_wishlist:
        if gt == "":
            gt = "No, Journey to the West is not in your wishlist"
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge
    else:
        return False
