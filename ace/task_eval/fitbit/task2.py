# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "View yesterday's health records on Fitbit.",
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
    Validates whether the user is viewing yesterday's health records on Fitbit.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions (not used in this task).

    Returns:
        bool: True if "Yesterday" is found, False otherwise.
    """
    # Initialize the XML parser
    parser = ETParser(xml)

    # Search for the element with the text "Yesterday"
    for el in parser.et.iter():
        if el.attrib.get("text") == "Yesterday":
            # print("Yesterday's health records are visible.")
            return True

    # If no matching element is found, return False
    # print("Yesterday's health records are not visible.")
    return False
