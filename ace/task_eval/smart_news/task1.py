# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "Open the headline of the top news in SmartNews",
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
    Validates that the user tapped within the 'top news' area on SmartNews.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including previous XML and actions.

    Returns:
        bool: True if the tap was within the bounds of the 'top news' area, False otherwise.
    """
    # Step 1: Parse the previous XML (-2 in history)
    try:
        news_tip = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        print("Previous XML data is missing in history.")
        return False

    # Step 2: Locate the 'top news' element using resource-id
    news_element = None
    for el in news_tip.et.iter():
        if el.attrib.get("resource-id") == "jp.gocro.smartnews.android:id/thumbnail":
            news_element = el
            break

    if news_element is None:
        # print("The 'top news' element was not found in the previous XML.")
        return False

    # Step 3: Get the parent element of the 'top news' element
    news_bound_element = news_tip.find_parent(news_element)

    # Extract bounds of the 'top news' element
    bounds = news_tip.get_bounds(news_bound_element)
    if not bounds:
        # print("Bounds for the 'top news' element could not be extracted.")
        return False

    x1, y1, x2, y2 = bounds
    # print(f"Top News Bounds: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

    # Step 4: Validate the tap location from the action history
    try:
        news_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data is missing in history.")
        return False

    # Check if the tap location is within the bounds
    if not (x1 <= news_action["x"] <= x2 and y1 <= news_action["y"] <= y2):
        # print("The tap action was not within the 'top news' bounds.")
        return False

    # If all validations pass
    return True
