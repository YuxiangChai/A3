# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task description.
    """
    return {
        "task": "Report today's calorie consumption from Fitbit.",
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
    Extracts and returns the calorie consumption from the XML data on Fitbit.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context (not used here).

    Returns:
        str: The calorie consumption value if found, or a message if not.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Define the resource-id to locate the calorie element
    resource_id = "secondary-focus-metric-2-calories"

    # Find the target element with the specified resource-id
    target_element = parser.get_element("resource-id", resource_id)
    if target_element is None:
        # print(f"Element with resource-id '{resource_id}' not found.")
        # return "Calorie consumption data not found."
        return False
    # Extract the text value for calories
    calories = target_element.attrib.get("text", "").strip()
    if not calories:
        # print("Calories data is missing or empty.")
        # return "No valid calorie data found."
        return False
    # Print and return the calorie consumption value
    # print(f"Calories consumed today: {calories}")
    gt = f"Calories consumed today: {calories}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
