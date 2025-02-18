# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the Settings in Gmail and tell me all email accounts.",
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
    Checks if the Gmail settings panel is open and retrieves the user's email addresses.

    Args:
        xml (str): Current XML content.
        screenshot (str): Screenshot content (unused in this task).
        history (dict): History of XML content (unused in this task).

    Returns:
        list: A list of email addresses found in the settings panel.
    """
    email_addresses = []

    try:
        # Step 1: Parse the current XML
        parser = ETParser(xml)
        # parser = ETParser(xml)

        # Step 2: Verify the settings panel is open
        settings_element = parser.get_element("text", "Settings")
        if settings_element is None:
            # print("Settings panel is not open.")
            return False

        # Step 3: Collect all elements with resource-id="com.google.android.gm:id/title"
        title_elements = [
            el.attrib.get("text", "").strip()
            for el in parser.et.iter()
            if el.attrib.get("resource-id", "") == "com.google.android.gm:id/title"
        ]

        # Step 4: Verify the first title is "General settings"
        if not title_elements or title_elements[0] != "General settings":
            # print("The first title is not 'General settings'. Exiting...")
            return False

        # Step 5: Extract email addresses until "Add account" is found
        for text in title_elements[1:]:  # Skip the first "General settings"
            if text == "Add account":
                break
            if text:  # Ignore empty strings
                email_addresses.append(text)

        # print(f"Email addresses found: {email_addresses}")
        gt = email_addresses
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    except Exception as e:
        # print(f"An error occurred during evaluation: {str(e)}")
        return False
