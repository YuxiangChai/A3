# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.a
    """
    return {
        "task": "Please tell me the rating of the nearest Starbucks on DoorDash.",
        "level": "easy",
        "category": "single-page query",
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
    Evaluates the XML to find the rating of the nearest Starbucks on DoorDash.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context (not used in this task).

    Returns:
        bool: True if the rating is successfully found, False otherwise.
    """
    # Step 1: Parse the XML to locate the element with resource-id "store_description_view"
    parser = ETParser(xml)
    tip_element = parser.get_element(
        "resource-id", "com.dd.doordash:id/store_description_view"
    )
    if tip_element is None:
        # print("Element with resource-id 'store_description_view' not found.")
        return False

    # Step 2: Find the parent element of the tip element
    parent_element = parser.find_parent(tip_element)
    if parent_element is None:
        # print("Parent element of 'store_description_view' not found.")
        return False

    # Step 3: Search within the parent element for the element with resource-id "rating_value"
    target_element = None
    for el in parent_element.iter():
        if el.attrib.get("resource-id") == "com.dd.doordash:id/rating_value":
            target_element = el
            break

    if target_element is None:
        # print("Element with resource-id 'rating_value' not found.")
        return False

    # Step 4: Extract and print the rating value
    rating_value = target_element.attrib.get("text", "").strip()
    if not rating_value:
        # print("Rating value not found.")
        return False

    # print("Rating value:", rating_value)

    gt = f"Rating value: {rating_value}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
