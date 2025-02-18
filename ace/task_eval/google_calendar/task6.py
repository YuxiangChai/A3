# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the 'Help & Feedback' section in Google Calendar.",
        "level": "easy",
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
    Evaluates whether the 'Help & Feedback' section in Google Calendar is open.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context (not used here).

    Returns:
        bool: True if the 'Help & Feedback' section is successfully opened, False otherwise.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Look for the element with the specified resource-id
    help_feedback_element = parser.get_element(
        "resource-id", "com.google.android.gms:id/gh_help_content"
    )

    if help_feedback_element is not None:
        # print("Successfully opened the 'Help & Feedback' section in Google Calendar.")
        return True
    else:
        # print("Failed to open the 'Help & Feedback' section in Google Calendar.")
        return False
