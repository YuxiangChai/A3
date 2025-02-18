# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Star the latest email in Gmail.",
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
    Evaluates whether the latest email in Gmail has been starred successfully.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context (not used here).

    Returns:
        bool: True if the latest email is starred, False otherwise.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Find the first element with the resource-id="com.google.android.gm:id/viewified_conversation_item_view"
    latest_email_element = None
    for el in parser.et.iter():
        if (
            el.attrib.get("resource-id")
            == "com.google.android.gm:id/viewified_conversation_item_view"
        ):
            latest_email_element = el
            break

    if latest_email_element is None:
        # print("No email element found in the current XML.")
        return False

    # Check if the element's text starts with "Starred,"
    text_value = latest_email_element.attrib.get("text", "").strip()
    if text_value.startswith("Starred,"):
        # print("The latest email has been successfully starred.")
        return True
    else:
        # print(f"The latest email is not starred. Current text: {text_value}")
        return False
