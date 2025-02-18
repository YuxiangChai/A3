# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.

    Task: Retrieve all tasks or holidays scheduled for December 25 in Google Calendar.

    Returns:
        dict: Task details including name, level, and category.
    """
    return {
        "task": "Retrieve all tasks or holidays scheduled for December 25 in Google Calendar.",
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
    Extracts tasks and holidays for December 25 based on XML content.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Optional, base64-encoded screenshot (not used here).
        history (dict): Contains historical data with keys:
                        - "xml": List of XML contents.
                        - "screenshot": List of screenshots.
                        - "actions": List of actions.

    Returns:
        list: A list containing the first two comma-separated fields from each matching content-desc.
    """
    # Parse the provided XML content
    parser = ETParser(xml)

    # Step 1: Locate the main container element
    container_element = parser.get_element(
        "resource-id",
        "com.google.android.calendar:id/alternate_timeline_fragment_container",
    )
    if container_element is None:
        # print("Error: Target container element not found.")
        return False

    # Step 2: Initialize variables
    found_open_day_view = False  # Flag to start collecting data
    items_list = []  # List to store extracted task or holiday details

    # Step 3: Search for '25 December 2024, Open Day View' and collect tasks/holidays
    for child in container_element:
        for sub_child in child:
            content_desc = sub_child.attrib.get("content-desc", "").strip()

            # Start collection when 'Open Day View' or 'Open Schedule View' is encountered
            if (
                "25 December 2024, Open Day View" in content_desc
                or "25 December 2024, Open Schedule View" in content_desc
            ):
                found_open_day_view = True
                # print("Found 'Open Day View' marker, starting collection...")
                continue

            # If flag is set, collect tasks until encountering an empty content-desc
            if found_open_day_view:
                if content_desc == "":
                    # print("Encountered empty content-desc, stopping collection.")
                    gt = "No tasks"  # Stop processing and return the results
                else:
                    # Split content-desc by commas and append the first two fields
                    split_fields = content_desc.split(",")
                    if len(split_fields) >= 2:
                        items_list.append(f"{split_fields[0]}, {split_fields[1]}")
                    elif len(split_fields) == 1:  # In case there's only one field
                        items_list.append(split_fields[0])

    # print("Collection complete.")
    gt = f"task lists: {items_list}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
