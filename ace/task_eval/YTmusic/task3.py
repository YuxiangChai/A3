# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open Taylor Swift's page on YouTube Music and subscribe.",
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
    Evaluates whether the task of subscribing to Taylor Swift on YouTube Music has been completed.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if the subscription was successful, False otherwise.
    """
    # Step 1: Confirm the action for "Taylor Swift" click is within bounds
    if len(history["actions"]) < 3:
        # print("Not enough actions in history.")
        return False

    taylor_action = history["actions"][-3]
    if not (63 <= taylor_action["x"] <= 1017 and 645 <= taylor_action["y"] <= 811):
        # print("The third last action was not within the 'Taylor Swift' region.")
        return False

    # Step 2: Confirm the action for "Subscribe" click is within bounds
    subscribe_action = history["actions"][-2]
    if not (
        53 <= subscribe_action["x"] <= 302 and 988 <= subscribe_action["y"] <= 1083
    ):
        # print("The second last action was not within the 'Subscribe' region.")
        return False

    # Step 3: Check previous XML for "Subscribe to Taylor Swift" button
    prev_parser = ETParser(history["xml"][-2])
    found_subscribe = any(
        "subscribe to taylor swift" in el.attrib.get("content-desc", "").strip().lower()
        for el in prev_parser.et.iter()
    )
    if not found_subscribe:
        # print(
        #     "The 'Subscribe to Taylor Swift' button was not found in the previous state."
        # )
        return False

    # Step 4: Check current XML for "Unsubscribe from Taylor Swift" button
    current_parser = ETParser(history["xml"][-1])
    found_unsubscribe = any(
        "unsubscribe from taylor swift"
        in el.attrib.get("content-desc", "").strip().lower()
        for el in current_parser.et.iter()
    )
    if found_unsubscribe:
        # print(
        #     "The 'Unsubscribe from Taylor Swift' button was found, indicating subscription is active."
        # )
        return True
    else:
        # print(
        #     "The 'Unsubscribe from Taylor Swift' button was not found in the final state."
        # )
        return False
