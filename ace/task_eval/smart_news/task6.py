# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "What is the release time of the headline of the top news in SmartNews",
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
    Extracts and returns the release time of the top news on SmartNews.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context (not used here).

    Returns:
        str: The release time of the top news if found, or an error message if not.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Define the resource-id to locate the timestamp of the top news
    resource_id = "jp.gocro.smartnews.android:id/timestamp"

    # Find the target element with the specified resource-id
    target_element = parser.get_element("resource-id", resource_id)
    if target_element is None:
        # print(f"Element with resource-id '{resource_id}' not found.")
        gt = "Top news release time not found."

    else:
        # Extract the text value from the element
        release_time = target_element.attrib.get("text", "").strip()
        if not release_time:
            # print("Release time data is missing.")
            gt = "No valid release time found."
        else:
            gt = f"Top News Release Time: {release_time}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
