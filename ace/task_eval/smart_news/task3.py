# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the personalized news section in SmartNews.",
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
    Evaluates whether the personalized news section has been successfully opened in SmartNews.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context (not used in this task).

    Returns:
        bool: True if the personalized news section is opened, False otherwise.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Check for the element with text="Personalize SmartNews"
    target_element = None
    for el in parser.et.iter():
        if el.attrib.get("text") == "Personalize SmartNews":
            target_element = el
            break

    if target_element is not None:
        # print("Successfully opened the personalized news section in SmartNews.")
        return True
    else:
        # print("Failed to open the personalized news section in SmartNews.")
        return False
