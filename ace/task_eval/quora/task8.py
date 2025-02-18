import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In Quora, navigate to Adam D'Angelo's profile and follow him",
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

    nav_bar_element = parser.get_element(
        "resource-id", "com.quora.android:id/navbar_start"
    )

    if nav_bar_element is None:
        return False

    profile_element = nav_bar_element.findall("*")[1]

    if profile_element.attrib["text"].lower() != "adam d'angelo":
        return False

    # the first toggle button must be follow button
    follow_button = parser.get_element("class", "android.widget.ToggleButton")

    if follow_button.attrib["text"].find("Following") == -1:
        return False

    return True
