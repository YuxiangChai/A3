import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open course 'cryptography' in 'learn' section tab in coursera app, and set a study reminder on every monday at 1:00pm",
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
    reminder_page_element = parser.get_element("text", "Study Reminders")

    if reminder_page_element is None:
        return False

    time_element = parser.get_element_contains_from_until(
        "resource-id",
        "org.coursera.android:id/timeText",
        "text",
        "Monday",
        "text",
        "Tuesday",
    )

    if time_element is None:
        return False

    if time_element.attrib["text"] != "01:00 PM":
        return False

    index = len(history["xml"]) - 1
    while index >= 0:
        index -= 1

        parser = ETParser(history["xml"][index])
        course_element = parser.get_element(
            "resource-id", "org.coursera.android:id/courseName"
        )

        if course_element is None:
            continue

        if course_element.attrib["text"].lower().find("cryptography") == -1:
            return False
        else:
            return True
    return False
