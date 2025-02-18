# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Search for 'sausage' in Target.",
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
    Validates whether the search action for 'sausage' in Target was successful.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the search for 'sausage' was successful, False otherwise.
    """
    # Parse the latest XML
    parser = ETParser(xml)

    # Locate the search input element by its text
    search_element = parser.get_element("text", "sausage")
    if search_element is None:
        # print("Search input element not found.")
        return False
    return True
