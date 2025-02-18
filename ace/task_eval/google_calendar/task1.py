from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Add an event titled 'Watching the NBA game' on January 14, 2025, from 10:00 AM to 11:30 AM to Google Calendar.",
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
    Evaluates whether the event has been successfully added to Google Calendar.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the event has been successfully added, False otherwise.
    """

    title_found = False
    date_time_found = False

    # Loop through all history XMLs to validate the two conditions
    for xml_data in history["xml"]:
        parser = ETParser(xml_data)

        # Condition 1: Check if the title exists
        title_element = parser.get_element(
            "resource-id", "com.google.android.calendar:id/title"
        )
        if (
            title_element is not None
            and title_element.attrib.get("text", "").strip() == "Watching the NBA game"
        ):
            title_found = True

        # Condition 2: Check if all the content-desc fields for date and time exist
        content_desc_values = [
            "Start date: Thu, Jan 14, 2025",
            "Start time: 10:00 AM",
            "End date: Thu, Jan 14, 2025",
            "End time: 11:30 AM",
        ]
        content_desc_found = all(
            parser.get_element("content-desc", desc) is not None
            for desc in content_desc_values
        )

        if title_found and content_desc_found:
            return True

    # If conditions are not satisfied
    # if not title_found:
    #     print("Title 'Watching the NBA game' not found in any history XML.")
    # if not date_time_found:
    #     print(
    #         "Required date and time content-desc values not found in any history XML."
    #     )

    return False
