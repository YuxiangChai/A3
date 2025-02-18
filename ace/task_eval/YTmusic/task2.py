# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Search for 'Taylor Swift' in YouTube Music.",
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
    Evaluates whether the search for 'Taylor Swift' has been performed on YouTube Music.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if 'Taylor Swift' is found in the search field, False otherwise.
    """
    # Initialize the XML parser
    parser = ETParser(xml)

    # Find the element with the specified resource-id
    element = parser.get_element(
        "resource-id", "com.google.android.apps.youtube.music:id/search_edit_text"
    )

    # Check if the element exists and its text matches "taylor swift"
    if element is not None and element.attrib.get("text", "").lower() == "taylor swift":
        return True

    # Return False if no matching element is found or text does not match
    return False
