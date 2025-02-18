# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task description.
    """
    return {
        "task": "Report today's running distance in kilometers from Fitbit.",
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
    Extracts and returns the running distance in kilometers from the XML data on Fitbit.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context (not used here).

    Returns:
        str: The running distance value if found, or a message if not.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Define the resource-id to locate the distance element
    resource_id = "secondary-focus-metric-1-distance"

    # Find the target element with the specified resource-id
    target_element = parser.get_element("resource-id", resource_id)
    if target_element is None:
        # print(f"Element with resource-id '{resource_id}' not found.")
        # return "Running distance data not found."
        return False
    # Extract the text value for distance
    distance = target_element.attrib.get("text", "").strip()
    if not distance:
        # print("Running distance data is missing or empty.")
        # return "No valid distance data found."
        return False
    # Print and return the running distance value
    # print(f"Running distance today: {distance}")
    gt = f"Running distance today: {distance}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
