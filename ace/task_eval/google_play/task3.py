# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Search for 'WhatsApp' on Google Play.",
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
    Evaluates whether 'WhatsApp' is displayed as a search result on Google Play.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if 'WhatsApp' is found, False otherwise.
    """
    # Initialize the XML parser
    parser = ETParser(xml)

    # Define the conditions to locate the element
    conditions = {
        "package": "com.android.vending",
        "class": "android.widget.TextView",
        "text": "whatsapp",
    }

    # Search for the element based on the specified conditions
    element = parser.get_element_bydic(conditions)

    # Return True if the element is found, otherwise False
    return element is not None
