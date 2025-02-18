# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "Open the Watch Apps category in Google Play's Apps section.",
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
    Verifies that the Watch Apps category is opened in Google Play.

    Args:
        xml (str): Current XML content.
        screenshot (str): Screenshot content (unused).
        history (dict): Historical data (unused).

    Returns:
        bool: True if Watch Apps category is successfully opened, False otherwise.
    """
    try:
        # Step 1: Parse the XML content
        with open(xml, "r", encoding="utf-8") as file:
            xml_content = file.read()
        parser = ETParser(xml_content)
        # print("Parsing XML to check for 'Watch apps' category...")

        # Step 2: Search for an element with text="" and content-desc="Watch apps"
        for element in parser.et.iter():
            text = element.attrib.get("text", "").strip()
            content_desc = element.attrib.get("content-desc", "").strip()

            if text == "" and content_desc == "Watch apps":
                # print("Success: Found 'Watch apps' category in the XML.")
                return True

        # If no matching element is found
        # print("Error: 'Watch apps' category not found in the XML.")
        return False

    except Exception as e:
        # print(f"An error occurred while evaluating: {str(e)}")
        return False
