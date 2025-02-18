# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "what is the number of new notifications in the Google Play Notifications section.",
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
    Evaluates the number of new notifications in the Google Play Notifications section.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the task is successfully evaluated, False otherwise.
    """
    notification_count = 0

    # Step 1: Iterate through all historical XMLs
    for idx, xml_data in enumerate(history["xml"]):
        parser = ETParser(xml_data)

        # Step 2: Find elements with content-desc starting with "Show notifications and"
        for el in parser.et.iter():
            content_desc = el.attrib.get("content-desc", "")
            if content_desc.startswith("Show notifications and"):
                # Check if it includes new notifications information
                if "new notifications available" in content_desc:
                    # Extract the number of notifications
                    try:
                        notification_count = int(
                            content_desc.split("new notifications available.")[0]
                            .split("Show notifications and offers.")[1]
                            .strip()
                        )
                        # print(
                        #     f"Detected {notification_count} new notifications in XML index {idx}."
                        # )
                        return True
                    except (IndexError, ValueError) as e:
                        # print(f"Error parsing notification count: {e}")
                        continue

    # Step 3: Output result
    if notification_count == 0:
        gt = "No new notifications detected in Google Play Notifications section."
    else:
        gt = f"{notification_count} notifications detected in Google Play Notifications section."
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
