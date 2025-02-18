import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Tell me how many percent of 'Magic Over Mind' I have read",
        "level": "middle",
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
    # parser = ETParser(xml)

    in_library = False
    in_home = False
    gt = ""
    for xml in history["xml"]:
        parser = ETParser(xml)
        if not in_home:
            home_element = parser.get_element(
                "resource-id", "com.google.android.apps.books:id/bottom_home"
            )

            if home_element is None:
                continue

            if home_element.attrib["selected"] != "true":
                continue

            in_home = True
        else:
            home_element = parser.get_element(
                "resource-id", "com.google.android.apps.books:id/bottom_home"
            )

            if home_element is None:
                in_home = False
                continue

            if home_element.attrib["selected"] != "true":
                in_home = False

            if in_home:
                book_element = parser.get_element_contains(
                    "content-desc", "Mind Over Magic"
                )

                if book_element is None:
                    continue

                gt = book_element.attrib["content-desc"]

        if not in_library:
            library_element = parser.get_element(
                "resource-id", "com.google.android.apps.books:id/bottom_library"
            )

            if library_element is None:
                continue

            if library_element.attrib["selected"] != "true":
                continue

            in_library = True

        else:
            library_element = parser.get_element(
                "resource-id", "com.google.android.apps.books:id/bottom_library"
            )

            if library_element is None:
                in_library = False
                continue

            if library_element.attrib["selected"] != "true":
                in_library = False

            if in_library:
                book_element = parser.get_element("text", "Mind Over Magic")

                if book_element is None:
                    continue

                book_parent = parser.find_parent(book_element)
                percentage_element = book_parent.findall("*")[2]
                gt = percentage_element.attrib["text"]

    if in_home or in_library:
        if gt == "":
            gt = "0.0"
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge
    else:
        judge = answer_correct_judge(
            task,
            answer,
            "not in home or library",
            client,
            model_type,
        )
        return judge
