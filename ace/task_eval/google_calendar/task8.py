# from a3.utils.xml_parser import ETParser
import re

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.

    Task: Check the number of scheduled items for December 25 in Google Calendar.
          Two possible cases need to be handled:
          1. A direct summary like "25 December: x items" in the content-desc attribute.
          2. A detailed day view containing specific tasks/events, counted between the 'Open Day View'
             marker and the first empty content-desc.

    Returns:
        dict: Task details including name, level, and category.
    """
    return {
        "task": "Check the number of scheduled items for December 25 in Google Calendar.",
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
    Evaluates the number of scheduled items for December 25 based on XML content.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Optional, base64-encoded screenshot (not used here).
        history (dict): Contains historical data with keys:
                        - "xml": List of XML contents.
                        - "screenshot": List of screenshots.
                        - "actions": List of actions.

    Returns:
        int: Number of scheduled items for December 25. Returns 0 if no valid content is found.
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
        gt = "0"

    # Step 2: Handle the first case - Check '25 December' or '25 December: x items'
    for child in container_element:
        for sub_child in child:
            content_desc = sub_child.attrib.get("content-desc", "").strip()

            # Split the content-desc and check the last two words
            content_desc_parts = content_desc.split()
            if len(content_desc_parts) >= 2 and content_desc_parts[-2:] == [
                "25",
                "December",
            ]:
                # print("Found '25 December': No items scheduled.")
                gt = "0"  # Zero items

            # Check for a summary like '25 December: x items' using regex
            match = re.search(r"25 December: (\d+) items", content_desc)
            if match:
                items_count = int(match.group(1))
                # print(f"Found '25 December' with {items_count} scheduled items.")
                gt = f"Found '25 December' with {items_count} scheduled items."
                judge = answer_correct_judge(
                    task,
                    answer,
                    gt,
                    client,
                    model_type,
                )
                return judge

    # Step 3: Handle the second case - Detailed day view
    found_open_day_view = False  # Flag to mark the start of 'Open Day View'
    items_count = 0  # Counter for tasks/items
    for child in container_element:
        for sub_child in child:
            content_desc = sub_child.attrib.get("content-desc", "").strip()

            # Check for '25 December 2024, Open Day View' or 'Open Schedule View'
            if (
                "25 December 2024, Open Day View" in content_desc
                or "25 December 2024, Open Schedule View" in content_desc
            ):
                found_open_day_view = True
                # print("Found 'Open Day View' marker, starting count...")
                continue  # Start counting subsequent elements

            # Count non-empty content-desc until encountering the first empty one
            if found_open_day_view:
                if content_desc == "":
                    # print(
                    #     f"Found {items_count} items between 'Open View' and the empty content-desc."
                    # )
                    gt = f"{items_count} items"
                    judge = answer_correct_judge(
                        task,
                        answer,
                        gt,
                        client,
                        model_type,
                    )
                    return judge
                if content_desc:  # Non-empty content-desc indicates a valid item/task
                    items_count += 1

    # Step 4: If no matches are found
    # print("No matching content found for 25 December.")
    return False
