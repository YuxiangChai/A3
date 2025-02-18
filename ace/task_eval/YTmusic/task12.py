# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "Search for the song 'Bad Guy' in YouTube Music. Tell me who is the singer, how long it lasts, and how many times it has been played.",
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
        str: The information about the specfic music if found, or a message if not.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Define the resource-id to locate the music-related message element
    resource_id = "com.google.android.apps.youtube.music:id/subtitle"

    # Find the target element with the specified resource-id
    target_element = parser.get_element("resource-id", resource_id)
    if target_element is None:
        # print(f"Element with resource-id '{resource_id}' not found.")
        gt = "gt not found."
    else:
        # Extract the text value
        gt = target_element.attrib.get("text", "").strip()
        if not gt:
            # print("Data is missing.")
            gt = "Not found"

    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
