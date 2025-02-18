from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Switch the calendar view to May 2026 in Google Calendar.",
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
    Evaluates whether the Google Calendar view has been successfully switched to May 2026.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context (not used here).

    Returns:
        bool: True if the calendar view is on May 2026, False otherwise.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Look for the element with the specified content-desc
    may_2026_element = parser.get_element("content-desc", "May 2026")

    if may_2026_element is not None:
        # print("Successfully switched the calendar view to May 2026.")
        return True
    else:
        # print("Failed to switch the calendar view to May 2026.")
        return False
