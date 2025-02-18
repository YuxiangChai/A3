# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Search for the event titled 'watch football game' and retrieve its scheduled time in Google Calendar.",
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
    target_event = "Watch football game"
    time_resource_id = "com.google.android.calendar:id/time"
    search_resource_id = "com.google.android.calendar:id/search_text"

    # Step 2: Iterate through all history XMLs
    for xml_data in history["xml"]:
        parser = ETParser(xml_data)

        # Step 3: Check for the target event title
        search_element = parser.get_element("resource-id", search_resource_id)
        if (
            search_element is not None
            and search_element.attrib.get("text", "").strip() == target_event
        ):
            # print(f"Found the event '{target_event}' .")
            break
    for xml_data in history["xml"]:
        parser = ETParser(xml_data)
        # Step 4: Find the time element in the same XML
        time_element = parser.get_element("resource-id", time_resource_id)
        if time_element is not None:
            event_time = time_element.attrib.get("text", "").strip()
            if event_time:
                # print(f"Scheduled time for '{target_event}' is: {event_time}")
                gt = f"Scheduled time for '{target_event}' is: {event_time}"
                judge = answer_correct_judge(
                    task,
                    answer,
                    gt,
                    client,
                    model_type,
                )
                return judge
            else:
                # print(f"Time element found, but event time is not correct.")
                return False
        else:
            # print(f"Time element with resource-id '{time_resource_id}' is not find.")
            return False

    # If no XML meets the criteria
    # print(
    #     f"Event '{target_event}' not found or time could not be retrieved in any history XML."
    # )
    return False
