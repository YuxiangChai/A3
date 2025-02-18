# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "View the first email in Gmail, open the sender's profile, and retrieve their email address.",
        "level": "hard",
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
    Retrieves the sender's email address by parsing the profile opened after clicking the avatar.

    Args:
        xml (str): Current XML content.
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Historical XML content (unused in this task).

    Returns:
        str: The sender's email address if found, otherwise an empty string.
    """
    try:
        # Step 1: Parse the current XML content
        parser = ETParser(xml)
        # print("Parsing XML to find the sender's email address...")

        # Step 2: Find the element with resource-id="com.google.android.gm:id/title"
        email_elements = [
            el.attrib.get("text", "").strip()
            for el in parser.et.iter()
            if el.attrib.get("resource-id", "") == "com.google.android.gm:id/title"
        ]

        # Step 3: Verify and return the email address
        if email_elements:
            sender_email = email_elements[
                0
            ]  # Assuming the first 'title' is the email address
            # print(f"Sender's email address found: {sender_email}")

            gt = sender_email
            judge = answer_correct_judge(
                task,
                answer,
                gt,
                client,
                model_type,
            )
            return judge

        # print("Error: Sender's email address not found.")
        return False

    except Exception as e:
        # print(
        #     f"An error occurred while retrieving the sender's email address: {str(e)}"
        # )
        return False
