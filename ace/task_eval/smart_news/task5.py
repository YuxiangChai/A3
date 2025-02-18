# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "What is the headline of the top news in SmartNews",
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
    Extracts and returns the headline of the top news on SmartNews.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context (not used here).

    Returns:
        str: The headline of the top news if found, or a message if not.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Define the resource-id to locate the top news headline
    resource_id = "jp.gocro.smartnews.android:id/title"

    # Find the target element with the specified resource-id
    target_element = parser.get_element("resource-id", resource_id)
    if target_element is None:
        # print(f"Element with resource-id '{resource_id}' not found.")
        return "Top news headline not found."

    # Extract the text value from the element
    headline = target_element.attrib.get("text", "").strip()
    if not headline:
        # print("Top news headline is missing.")
        gt = "No valid headline found."

    # Print and return the headline
    # print(f"Top News Headline: {headline}")
    else:
        gt = f"Top News Headline: {headline}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
