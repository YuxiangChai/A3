# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Start an exercise in Fitbit, then select 'Walk' to begin the activity.",
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
    Validates whether an exercise activity is active and 'Walk' is selected in Fitbit.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the exercise activity is active with 'Walk' selected, False otherwise.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Step 1: Check for the presence of elements with content-desc="Pause" and content-desc="Walk"
    pause_found = False
    walk_found = False
    for el in parser.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if content_desc == "Pause":
            pause_found = True
        elif content_desc == "Walk":
            walk_found = True
        # Stop searching if both elements are found
        if pause_found and walk_found:
            break

    # Step 2: Validate the presence of both elements
    if pause_found and walk_found:
        # print("Exercise activity is currently active with 'Walk' selected.")
        return True
    else:
        # print("Exercise activity is not active with 'Walk' selected.")
        return False
