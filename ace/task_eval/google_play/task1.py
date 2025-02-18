# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {"task": "Open Google Play.", "level": "easy", "category": "operation"}


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
    Validates whether the Google Play homepage is opened by checking the presence
    of specific text elements.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if all required elements are found, False otherwise.
    """
    # Initialize the XML parser
    parser = ETParser(xml)

    # Define the required text values to match
    required_texts = {"games", "apps", "books", "search", "offers"}

    # Iterate through all elements to find matches
    for el in parser.et.iter():
        if (
            el.tag == "android.widget.TextView"
            and el.attrib.get("package") == "com.android.vending"
            and el.attrib.get("class") == "android.widget.TextView"
        ):
            # Check if the element's text is in the required_texts set
            text_value = el.attrib.get("text", "").lower()
            if text_value in required_texts:
                required_texts.remove(text_value)  # Remove matched text

            # If all required texts are matched, return True
            if not required_texts:
                return True

    # Return False if not all required texts are matched
    return False
