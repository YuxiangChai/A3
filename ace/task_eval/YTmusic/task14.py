# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "How long is the duration of the current playing song on YouTube Music.",
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
    Extracts and returns the total duration of the currently playing song from the XML data.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context (not used here).

    Returns:
        str: The total duration of the playing song, or an error message if not found.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Define the resource-id to locate the time information
    resource_id = "com.google.android.apps.youtube.music:id/time_bar"

    # Find the target element with the specified resource-id
    target_element = parser.get_element("resource-id", resource_id)
    if target_element is None:
        # print(f"Element with resource-id '{resource_id}' not found.")
        gt = "Not found."
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    # Extract the text value
    text = target_element.attrib.get("content-desc", "").strip()
    if not text:
        # print("Song duration data is missing.")
        gt = "Not found."
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    # Extract the total duration part (e.g., "2 minutes 57 seconds" from "0 minutes 5 seconds of 2 minutes 57 seconds")
    if "of" in text:
        gt = text.split("of")[-1].strip()
    else:
        gt = text  # If "of" is not in the text, assume it contains only total duration

    # Print and return the total duration
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
