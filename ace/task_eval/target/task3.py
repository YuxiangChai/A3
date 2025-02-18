# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Favorite the first sausage in the sorted 'Best Selling' list in Target.",
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
    Evaluates the task of favoriting the first sausage in the sorted 'Best Selling' list.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context (not used in this task).

    Returns:
        bool: True if the first sausage is successfully marked as favorite, False otherwise.
    """

    # Step 1: Parse the XML to find the first element with resource-id "com.target.ui:id/favorites_icon"
    parser = ETParser(xml)
    favorite_icon_element = parser.get_element(
        "resource-id", "com.target.ui:id/favorites_icon"
    )

    if favorite_icon_element is None:
        # print("Favorite icon element not found.")
        return False

    # Step 2: Check the content-desc attribute to determine if the item is "Favorite" or "Unfavorite"
    content_desc = favorite_icon_element.attrib.get("content-desc", "").strip()
    if not content_desc:
        # print("Content description is missing.")
        return False

    # Extract the first word from the content-desc text
    status = content_desc.split(" ")[0].lower()
    if status == "favorite":
        # print("The first sausage is already marked as 'Unfavorite'. Task failed.")
        return False
    elif status == "unfavorite":
        # print("The first sausage is successfully marked as 'Favorite'. Task succeeded.")
        return True
    else:
        # print("Unknown status in content-desc.")
        return False
