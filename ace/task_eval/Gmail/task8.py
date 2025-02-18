# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.screenshot_ocr import process_screenshot_with_bounds
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the first e-mail in Gmail and retrieve its content.",
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
    Verifies that the first email in Gmail was opened and retrieves its content.

    Args:
        xml (str): Current XML content (unused).
        screenshot (str): Screenshot of the opened email.
        history (dict): Historical XML content and actions:
                        - "xml": List of XML file paths.
                        - "actions": List of user actions (e.g., taps with coordinates).

    Returns:
        str: Extracted text content of the email.
    """
    try:
        # Step 1: Validate tap on the first email item (xml[-3])
        try:
            xml3 = history["xml"][-2]
            email_list_xml = ETParser(xml3)
        except (KeyError, IndexError):
            # print("Error: Missing XML data for email list.")
            return False

        email_item_element = email_list_xml.get_element(
            "resource-id", "com.google.android.gm:id/viewified_conversation_item_view"
        )
        if email_item_element is None:
            # print("First email item not found in the email list XML.")
            return False

        # Extract bounds and check action
        email_bounds_str = email_item_element.attrib.get("bounds", "")
        try:
            email_bounds = tuple(
                map(int, email_bounds_str.strip("[]").replace("][", ",").split(","))
            )
        except ValueError:
            # print("Invalid bounds format for the first email item.")
            return False

        first_email_action = history["actions"][-2]
        if not (
            email_bounds[0] <= first_email_action["x"] <= email_bounds[2]
            and email_bounds[1] <= first_email_action["y"] <= email_bounds[3]
        ):
            # print(
            #     "The tap action for the first email item is outside the expected bounds."
            # )
            return False

        # Step 2: Extract bounds from show_hide_details and conversation_webview (xml[-2])
        try:
            email_opened_xml = ETParser(xml)
        except (KeyError, IndexError):
            # print("Error: Missing XML data for opened email.")
            return False

        # Get bounds of 'show_hide_details'
        details_element = email_opened_xml.get_element(
            "resource-id", "com.google.android.gm:id/show_hide_details"
        )
        if details_element is None:
            # print("Error: 'show_hide_details' element not found.")
            return False

        details_bounds_str = details_element.attrib.get("bounds", "")
        try:
            _, _, _, y2 = map(
                int, details_bounds_str.strip("[]").replace("][", ",").split(",")
            )
        except ValueError:
            # print("Error: Invalid bounds format for 'show_hide_details'.")
            return False

        # Get bounds of 'conversation_webview'
        webview_element = email_opened_xml.get_element(
            "resource-id", "com.google.android.gm:id/conversation_topmost_overlay"
        )
        if webview_element is None:
            # print("Error: 'conversation_webview' element not found.")
            return False

        webview_bounds_str = webview_element.attrib.get("bounds", "")
        try:
            x1, _, x2, y3 = map(
                int, webview_bounds_str.strip("[]").replace("][", ",").split(",")
            )
            final_bounds = (x1, y2, x2, y3)  # Update upper boundary
        except ValueError:
            # print("Error: Invalid bounds format for 'conversation_webview'.")
            return False

        # Step 3: Extract email content using OCR
        email_content = process_screenshot_with_bounds(screenshot, final_bounds)
        # print(email_content)
        gt = email_content
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            model_type,
        )
        return judge

    except Exception as e:
        # print(f"An error occurred during evaluation: {str(e)}")
        return False
