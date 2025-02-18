# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "Open the Ratings and Reviews section of 'WhatsApp' in Google Play.",
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
    Verifies that the Ratings and Reviews section of WhatsApp is opened in Google Play.

    Args:
        xml (str): Current XML content.
        screenshot (str): Screenshot content (unused).
        history (dict): Historical data (unused).

    Returns:
        bool: True if the target Ratings and Reviews section is found, False otherwise.
    """
    try:
        parser = ETParser(xml)

        target_keywords = ["WhatsApp Messenger", "Ratings and Reviews"]
        for element in parser.et.iter():
            content_desc = element.attrib.get("content-desc", "").strip()
            # Check if all target keywords are in the content-desc
            if all(keyword in content_desc for keyword in target_keywords):
                return True

        # If no matching element is found
        # print("Error: 'Ratings and Reviews' section for WhatsApp not found in the XML.")
        return False

    except Exception as e:
        # print(f"An error occurred during evaluation: {str(e)}")
        return False
