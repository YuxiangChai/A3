# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Subscribe to the YouTuber currently playing on the Shorts section in YouTube.",
        "level": "medium",
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
    Evaluates whether the user successfully subscribed to the YouTuber playing on the Shorts section.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the user successfully subscribed, False otherwise.
    """
    if len(history["xml"]) < 2:
        # print("Not enough XML history to evaluate the task.")
        return False

    # Step 1: Check the XML at index -2 for the "Subscribe" button
    parser_prev = ETParser(history["xml"][-2])

    subscribe_element = None
    for el in parser_prev.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if content_desc.startswith("Subscribe to"):
            subscribe_element = el
            subscribed_to = content_desc.split("Subscribe to")[1].strip()
            # print(f"Found subscription target: {subscribed_to}")
            break

    if subscribe_element is None:
        # print("No 'Subscribe to ...' button found in XML index -2.")
        return False

    # Step 2: Check the XML at index -1 for the "Unsubscribe" confirmation
    parser_current = ETParser(history["xml"][-1])

    for el in parser_current.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if content_desc.startswith("Unsubscribe from"):
            unsubscribed_from = content_desc.split("Unsubscribe from")[1].strip()
            if unsubscribed_from == subscribed_to:
                # print(f"Subscription to {unsubscribed_from} successfully confirmed.")
                return True

    # print("Subscription confirmation not found in XML index -1.")
    return False
