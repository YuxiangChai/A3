import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search for 'Artificial Intelligence' on Quora and set filter to show topics only. Then follow the topic 'Artificial Intellegence'.",
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

    filter_element = parser.get_element("text", "Clear Filters")

    if filter_element is None:
        return False

    # from end to beginning, topics filter must be selected at end.
    index = len(history["xml"]) - 1
    while index >= 0:
        index -= 1
        parser = ETParser(history["xml"][index])

        topic_filter_element = parser.get_element("text", "Topics")

        if topic_filter_element is None:
            continue

        if topic_filter_element.attrib["focused"] == "false":
            return False
        else:
            return True

    return False
