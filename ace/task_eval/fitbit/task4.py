# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "View calorie consumption in Fitbit and switch to the weekly view.",
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
    """
    Validates whether the weekly view for calorie consumption is selected in Fitbit.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the weekly view is selected, False otherwise.
    """
    # Step 1: Initialize XML parser
    parser = ETParser(xml)
    target_text = "Week".strip().lower()

    # Step 2: Find the parent element of the element with text="Week"
    parent_element = None
    for parent in parser.et.iter():
        for el in parent:
            text = el.attrib.get("text", "").strip().lower()
            if text == target_text:
                parent_element = parent
                break
        if parent_element:
            break

    if not parent_element:
        # print("Element with text 'Week' or its parent not found.")
        return False

    # Step 3: Check if the parent element has clickable="false"
    if parent_element.attrib.get("clickable") == "false":
        # print("Weekly view is selected.")
        return True
    else:
        # print("Weekly view is not selected.")
        return False
