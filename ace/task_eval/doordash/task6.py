# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task description.
    """
    return {
        "task": "Open the 'Sports' section within the 'Browse' category in DoorDash.",
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
    Evaluates whether the 'Sports' section in the 'Browse' category has been successfully opened in DoorDash.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context with XMLs and actions.

    Returns:
        bool: True if the 'Sports' section is successfully opened, False otherwise.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Step 1: Check if the 'Sports' section is open
    sports_section = parser.get_element_bydic(
        {
            "text": "Sports",
            "resource-id": "com.dd.doordash:id/textView_navBar_backdropTitle",
        }
    )

    if sports_section is None:
        # print("The 'Sports' section is not open.")
        return False

    # Step 2: Check if the 'Browse' category is selected
    browse_element = parser.get_element_bydic(
        {"resource-id": "com.dd.doordash:id/browse", "selected": "true"}
    )

    if browse_element is None:
        # print("The 'Browse' category is not selected.")
        return False

    # If both checks pass, return True
    # print("Successfully opened the 'Sports' section in the 'Browse' category.")
    return True
