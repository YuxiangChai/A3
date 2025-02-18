# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the Notifications section in Google Maps.",
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
    Evaluates whether the Notifications section in Google Maps has been successfully opened.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the Notifications section is opened, False otherwise.
    """
    # Step 1: Parse the current XML
    parser = ETParser(xml)

    # Step 2: Look for the element with text="Notifications" and resource-id="com.google.android.apps.maps:id/title"
    for el in parser.et.iter():
        if (
            el.attrib.get("text", "") == "Notifications"
            and el.attrib.get("resource-id", "")
            == "com.google.android.apps.maps:id/title"
        ):
            # print("Notifications section in Google Maps is successfully opened.")
            return True

    # Step 3: If not found, return False
    # print("Notifications section in Google Maps is not opened.")
    return False
