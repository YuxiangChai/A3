import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search 'linear algebra' at 'beginner level' in Coursera app.",
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
    search_element = parser.get_element("text", "Search")
    if search_element is None:
        return False

    search_la_element = parser.get_element("class", "android.widget.EditText")

    if search_la_element is None:
        return False

    if search_la_element.attrib["text"].lower() != "linear algebra":
        return False

    filter_element = parser.get_element_contains("content-desc", "Filter")

    if filter_element is None:
        return False

    index = len(history["xml"]) - 1
    while index >= 0:
        index -= 1
        parser = ETParser(history["xml"][index])

        filter_top_element = parser.get_element("text", "Filter")

        if filter_top_element is None:
            continue
        else:
            level_element = parser.get_element("text", "Level")

            if level_element is None:
                continue
            index_of_level = level_element.attrib["index"]

            index_of_beginner = int(index_of_level) + 3

            beginner_element = parser.get_element("index", f"{index_of_beginner}")

            if beginner_element is None:
                continue
            else:
                if beginner_element.attrib["checked"] == "true":
                    return True
                else:
                    return False

    return False
