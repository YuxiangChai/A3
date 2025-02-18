# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the Drafts folder in Gmail",
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
    Checks whether the Drafts folder is opened in Gmail.

    Args:
        xml (str): Current XML content (unused in this task).
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Historical XML content with keys:
                        - "xml": List of XML file paths.

    Returns:
        bool: True if the Drafts folder is detected, False otherwise.
    """
    try:
        parser = ETParser(xml)

        # Step 2: Search for the element with the required conditions
        drafts_element = parser.get_element(
            "resource-id", "com.google.android.gm:id/conversation_list_folder_name"
        )
        if (
            drafts_element is not None
            and drafts_element.attrib.get("text", "").strip() == "Drafts"
        ):
            # print("Found 'Drafts' folder in XML.")
            return True

        # If no valid 'Drafts' element is found
        # print("Drafts folder not found in any XML files.")
        return False

    except Exception as e:
        # print(f"Error occurred during evaluation: {str(e)}")
        return False
