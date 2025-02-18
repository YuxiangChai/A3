# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "View the personal information in Fitbit.",
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
    Validates whether the 'Personal' information is displayed in Fitbit.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if 'Personal' information is found, False otherwise.
    """
    # Parse the XML
    parser = ETParser(xml)

    # Search for the element with text="Personal"
    for el in parser.et.iter():
        if el.attrib.get("text") == "Personal":
            return True

    # If no matching element is found, return False
    return False
