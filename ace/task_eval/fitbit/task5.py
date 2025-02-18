# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the 'Customize Today' section in Fitbit.",
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
    Evaluates whether the 'Customize Today' section in Fitbit is open.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions (not used here).

    Returns:
        bool: True if the 'Customize Today' section is open, False otherwise.
    """
    # Step 1: Parse the current XML
    parser = ETParser(xml)

    # Step 2: Find the element with text="Customize Today"
    customize_today_element = parser.get_element("text", "Customize Today")

    if customize_today_element is not None:
        # print("The 'Customize Today' section is open.")
        return True
    else:
        # print("The 'Customize Today' section is not detected.")
        return False
