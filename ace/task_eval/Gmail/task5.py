# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Tell me the number of unread emails in Gmail.",
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
    Evaluates the number of unread emails in Gmail by analyzing historical XMLs.

    Args:
        xml (str): Current XML content as a string (not used here).
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context containing XMLs.

    Returns:
        str: The number of unread emails if found, otherwise an appropriate message.
    """
    # Iterate over the historical XMLs
    for idx, xml_data in enumerate(history["xml"]):
        parser = ETParser(xml_data)

        # Traverse all elements to find those with content-desc starting with "Mail,"
        for el in parser.et.iter():
            content_desc = el.attrib.get("content-desc", "")
            if content_desc.startswith("Mail,"):
                # print(f"Found mail notification in XML index {idx}: {content_desc}")
                gt = f"{content_desc} unread mails"
                judge = answer_correct_judge(
                    task,
                    answer,
                    gt,
                    client,
                    model_type,
                )
                return judge

    # If no matching XML is found
    gt = "No unread emails detected in Gmail."
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
