# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "What is the headline of the top news in the Sports section in SmartNews.",
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
    Extracts and returns the headline of the top news in the Sports section on SmartNews.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context (not used here).

    Returns:
        str: The headline of the top news in Sports if found, or an error message if not.
    """
    # Initialize XML parser
    parser = ETParser(xml)

    # Step 1: Check if the "Sports" section is selected
    section_name = "Sports"
    section_element = parser.get_element("text", section_name)
    if section_element is None:
        # print(f"Element with text '{section_name}' not found.")
        gt = "Sports section not found."

    # Check if the Sports section is currently selected
    is_selected = section_element.attrib.get("selected", "")
    if is_selected.lower() != "true":
        # print("Sports section is not selected.")
        gt = "Sports section is not selected."

    # Step 2: Locate the headline of the top news in the Sports section
    resource_id = "jp.gocro.smartnews.android:id/title"
    headline_element = parser.get_element("resource-id", resource_id)
    if headline_element is None:
        # print(f"Element with resource-id '{resource_id}' not found.")
        gt = "Top news headline in Sports section not found."

    # Extract the text value from the element
    headline = headline_element.attrib.get("text", "").strip()
    if not headline:
        # print("Headline text is missing.")
        gt = "No valid headline found."
    else:
        # Print and return the headline
        # print(f"Sports News Headline: {headline}")
        gt = f"Sports News Headline: {headline}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
