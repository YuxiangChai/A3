# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "View the information about the connected devices in Fitbit.",
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
    Validates whether the "Connected to Fitbit" information is displayed in Fitbit.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if "Connected to Fitbit" information is found, False otherwise.
    """
    # Step 1: Parse the XML
    parser = ETParser(xml)

    # Step 2: Search for the element with text="Connected to Fitbit"
    for el in parser.et.iter():
        if el.attrib.get("text") == "Connected to Fitbit":
            # print("'Connected to Fitbit' information is displayed.")
            return True

    # If no matching element is found, return False
    # print("'Connected to Fitbit' information is not detected.")
    return False
