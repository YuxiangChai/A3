# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Reorder the sections in the Personalized News section of SmartNews by dragging section blocks so that the first three sections are: Top News, Sports, Politics.",
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
    Evaluates whether the first three sections in the Personalized News section of SmartNews have been reordered correctly.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the first three sections are correctly reordered, False otherwise.
    """
    # Define the expected order of the first three sections
    expected_order = ["Top News", "Sports", "Politics"]

    # Parse the latest XML
    parser = ETParser(xml)

    # Step 1: Collect the first three section names
    section_names = []
    for el in parser.et.iter():
        if el.attrib.get("resource-id") == "jp.gocro.smartnews.android:id/nameTextView":
            text_value = el.attrib.get("text", "").strip()
            if text_value:
                section_names.append(text_value)
                if len(section_names) == 3:  # Stop after collecting three sections
                    break

    # Step 2: Compare the collected section names with the expected order
    if section_names == expected_order:
        # print("Sections are correctly reordered to: Top News, Sports, Politics.")
        return True
    else:
        # print(f"Section order is incorrect. Current order: {section_names}")
        return False
