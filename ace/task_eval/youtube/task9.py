# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the Shorts section on YouTube and tell me the number of comments on the currently playing video.",
        "level": "medium",
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
    Evaluates whether the number of comments on the current Shorts video can be retrieved.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions (not used here).

    Returns:
        bool: True if the number of comments is successfully retrieved, False otherwise.
    """
    parser = ETParser(xml)

    # Step 1: Search for an element with content-desc starting with "View" and ending with "comments"
    comments_element = None
    for el in parser.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if content_desc.startswith("View") and content_desc.endswith("comments"):
            comments_element = el
            break

    if comments_element is None:
        # print("No element with content-desc matching 'View ... comments' found.")
        return False

    # Step 2: Extract the number of comments from the content-desc
    content_desc = comments_element.attrib["content-desc"]
    try:
        # Extract the number using string manipulation
        comment_count = content_desc.split(" ")[1].replace(",", "")
        # print(f"Number of comments: {comment_count}")
        gt = f"Number of comments: {comment_count}"
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge
    except (IndexError, ValueError) as e:
        # print(f"Failed to extract the number of comments: {e}")
        return False
