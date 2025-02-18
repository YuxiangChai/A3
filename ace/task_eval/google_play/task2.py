# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the Notifications section in Google Play.",
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
    Evaluates whether the Notifications section in Google Play has been successfully opened.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the Notifications section is opened, False otherwise.
    """
    # Step 1: Parse the last XML
    parser = ETParser(xml)

    # Step 2: Check for elements with "text" containing "Notifications" and "offers"
    found_notifications = False
    found_offers = False

    for el in parser.et.iter():
        text = el.attrib.get("text", "").lower()
        if "notifications" in text:
            found_notifications = True
        if "offers" in text:
            found_offers = True
        if found_notifications and found_offers:
            # print("Notifications and offers detected in the XML.")
            return True

    # Step 3: If not found, return False
    # if not found_notifications:
    # print("Notifications text not found in the XML.")
    # if not found_offers:
    # print("Offers text not found in the XML.")
    return False
