# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {"task": "Open YouTube Music.", "level": "easy", "category": "operation"}


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
    Evaluates whether YouTube Music is open and verifies the presence of specific tabs.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if all required tabs are found, False otherwise.
    """
    # Initialize the XML parser
    parser = ETParser(xml)

    # Define the required text values to match
    required_texts = {"home", "samples", "upgrade", "library", "explore"}

    # Iterate through elements to find matches
    for el in parser.et.iter():
        if (
            el.attrib.get("resource-id")
            == "com.google.android.apps.youtube.music:id/text1"
        ):
            # Check if the element's text matches any required text
            text_value = el.attrib.get("text", "").lower()
            if text_value in required_texts:
                required_texts.remove(text_value)  # Remove matched text

            # If all required texts are matched, return True
            if not required_texts:
                return True

    # Return False if not all required texts are matched
    return False
