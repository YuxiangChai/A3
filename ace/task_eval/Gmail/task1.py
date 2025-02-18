# from a3.utils.xml_parser import ETParser
from ace.utils.screenshot_ocr import process_screenshot_with_bounds
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Send an email to 'autoreply002@hotmail.com', with subject: 'Meeting', content: 'Lets meet next Saturday'",
        "level": "hard",
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
    Validates that an email with the correct subject, recipient, and content was composed and sent in Gmail.

    Args:
        xml (str): Current XML content (unused).
        screenshot (str): Screenshot of the compose email screen.
        history (dict): History containing:
                        - "xml": List of XML files.
                        - "actions": List of user actions (e.g., taps with coordinates).

    Returns:
        bool: True if all conditions are met, False otherwise.
    """
    try:
        # Step 1: Analyze the last editing screen (xml[-2])
        xml_path = history["xml"][-2]
        compose_email_xml = ETParser(xml_path)
        # compose_email_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Compose email XML is missing.")
        return False

    # Step 2: Validate the email subject
    subject_element = compose_email_xml.get_element(
        "resource-id", "com.google.android.gm:id/subject"
    )
    if subject_element is None or subject_element.attrib.get("text", "") != "Meeting":
        # print("Subject is incorrect or missing.")
        return False

    # Step 3: Validate the recipient email address
    recipient_element = compose_email_xml.get_element(
        "resource-id", "com.google.android.gm:id/peoplekit_chip"
    )
    if (
        recipient_element is None
        or recipient_element.attrib.get("text", "") != "autoreply002@hotmail.com"
    ):
        # print("Recipient email address is incorrect or missing.")
        return False

    body_element = compose_email_xml.get_element(
        "resource-id", "com.google.android.gm:id/compose_body_parent"
    )
    if body_element is None:
        # print("Email body element not found.")
        return False

    # Extract bounds and apply OCR
    body_bounds_str = body_element.attrib.get("bounds", "")
    try:
        body_bounds = tuple(
            map(int, body_bounds_str.strip("[]").replace("][", ",").split(","))
        )
    except ValueError:
        # print("Invalid bounds format for email body.")
        return False

    email_body_text = process_screenshot_with_bounds(
        history["screenshot"][-2], body_bounds
    )
    if "Let's meet next Saturday" not in email_body_text:
        # print("Email content is incorrect.")
        return False

    # Step 5: Validate the send action
    send_element = compose_email_xml.get_element(
        "resource-id", "com.google.android.gm:id/send"
    )
    if send_element is None:
        # print("Send button not found.")
        return False

    send_bounds_str = send_element.attrib.get("bounds", "")
    try:
        send_bounds = tuple(
            map(int, send_bounds_str.strip("[]").replace("][", ",").split(","))
        )
    except ValueError:
        # print("Invalid bounds format for send button.")
        return False

    # Retrieve the action corresponding to tapping "send"
    try:
        send_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Send action is missing in history.")
        return False

    # Validate if the tap action is within the bounds
    if not (
        send_bounds[0] <= send_action["x"] <= send_bounds[2]
        and send_bounds[1] <= send_action["y"] <= send_bounds[3]
    ):
        # print("The tap action for 'Send' was not within the expected bounds.")
        return False

    # All checks passed
    # print(
    #     "Email was composed and sent successfully with correct subject, recipient, and content."
    # )
    return True
