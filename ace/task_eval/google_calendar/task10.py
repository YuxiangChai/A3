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
        "task": "Count the total number of tasks and events for December in Google Calendar.",
        "level": "medium",
        "category": "multi-page query",
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
    Counts the total number of tasks and events for December from the provided XML history.

    Args:
        xml (str): Current XML content (unused in this task).
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Contains historical XML data.

    Returns:
        int: Total number of tasks and events for December across all valid XML files.
    """
    total_items = 0  # Accumulator for all items

    # Regex pattern for exclusion: "Weekday Number Month"
    pattern = re.compile(
        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) \d+ (January|February|March|April|May|June|July|August|September|October|November|December)"
    )

    # Iterate through each XML file in history
    for idx, xml_data in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_data)

            # Step 1: Check for "December" date picker element
            date_picker_element = parser.get_element(
                "resource-id", "com.google.android.calendar:id/date_picker_text_view"
            )
            if (
                date_picker_element is None
                or date_picker_element.attrib.get("text", "").strip() != "December"
            ):
                # print(f"[{idx}] 'December' date picker element not found. Skipping...")
                continue  # Skip to the next XML file

            # print(f"[{idx}] Found 'December' in the date picker. Proceeding...")

            # Step 2: Locate the main container element
            container_element = parser.get_element(
                "resource-id",
                "com.google.android.calendar:id/alternate_timeline_fragment_container",
            )
            if container_element is None:
                # print(f"[{idx}] Timeline container element not found. Skipping...")
                continue
            correct_xml = True
            # Step 3: Traverse and count valid items
            for child in container_element:
                for sub_child in child:
                    content_desc = sub_child.attrib.get("content-desc", "").strip()

                    # Apply exclusion rule: Match "Weekday Number Month"
                    if not pattern.match(content_desc):
                        correct_xml = False  # Skip invalid content-desc

                    # Check if content-desc contains "December" and ends with "item" or "items"
                    if "December" in content_desc:
                        match = re.search(r"(\d+) item(s?)", content_desc)
                        if match:
                            count = int(match.group(1))
                            total_items += count
                        # print(f"[{idx}] Counted {count} items from: '{content_desc}'")
            if correct_xml:
                # print(f"Total number of tasks and events for December: {total_items}")
                gt = f"Total number of tasks and events for December: {total_items}"
                judge = answer_correct_judge(
                    task,
                    answer,
                    gt,
                    client,
                    model_type,
                )
                return judge
            else:
                total_items = 0
                continue

        except Exception as e:
            # print(f"[{idx}] Error processing XML '{xml_data}': {str(e)}. Skipping...")
            continue

    # Print the total count across all XML files

    gt = f"Total number of tasks and events for December: {total_items}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
