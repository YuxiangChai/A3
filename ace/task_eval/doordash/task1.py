# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Search for 'Pizza' in DoorDash.",
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
    Validates whether the search action for 'Pizza' in DoorDash was successful.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the search for 'Pizza' was successful, False otherwise.
    """
    # Parse the latest XML
    parser = ETParser(xml)

    # Locate the search input element by its resource-id
    search_element = None
    for el in parser.et.iter():
        if el.attrib.get("resource-id") == "com.dd.doordash:id/edit_text":
            search_element = el
            break

    if search_element is None:
        # print("Search input element not found.")
        return False

    # Check if the search text matches "Pizza"
    search_text = search_element.attrib.get("text", "").strip()
    if search_text == "Pizza":
        # print("Search action for 'Pizza' was successful.")
        return True
    else:
        # print(f"The search text is '{search_text}' instead of 'Pizza'.")
        return False
