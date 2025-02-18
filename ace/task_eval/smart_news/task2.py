# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "Switch news section to Sports in SmartNews",
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

    # Define the TEXT to locate the top news headline
    text = "Sports"

    # Find the target element with the specified TEXT
    target_element = parser.get_element("text", text)
    if target_element is None:
        # print(f"Element with TEXT '{text}' not found.")
        return "Sports not found."

    # Extract the text value from the elementselected="false"
    headline = target_element.attrib.get("selected", "")
    if headline == "false":
        # print("Sports not choose.")
        return False

    # Print and return the headline
    # print(f"Top News Headline: {headline}")
    return True
