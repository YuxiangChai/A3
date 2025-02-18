# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {"task": "Open Fitbit", "level": "easy", "category": "operation"}


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
    Validates whether the Fitbit app is currently open by checking the XML structure.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions (not used in this task).

    Returns:
        bool: True if the Fitbit app is open, False otherwise.
    """
    # Initialize the XML parser
    parser = ETParser(xml)

    # Search for the element with the specific resource-id
    for el in parser.et.iter():
        if el.attrib.get("resource-id") == "com.fitbit.FitbitMobile:id/action_bar_root":
            # print("Fitbit app is open.")
            return True

    # If no matching element is found, return False
    # print("Fitbit app is not open.")
    return False
