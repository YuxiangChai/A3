# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Get opening hours of the first three stores in DoorDash Shopping area.",
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
    Extracts the opening hours of the first three stores in the Shopping area of DoorDash.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used in this task).
        history (dict): Historical context with XMLs and actions.

    Returns:
        list[str]: A list containing the opening hours of the first three stores.
    """
    # Initialize the list to store opening hours
    opening_hours = []

    # Iterate over historical XMLs to find the correct one
    for xml_data in history["xml"]:
        parser = ETParser(xml_data)

        # Traverse elements to find the correct area
        is_shopping_area = False
        for el in parser.et.iter():
            if (
                el.attrib.get("resource-id") == "com.dd.doordash:id/title"
                and el.attrib.get("text", "").strip() == "Shopping"
            ):
                is_shopping_area = True
                break

        if not is_shopping_area:
            continue

        # Traverse again to find the opening hours
        count = 0
        for el in parser.et.iter():
            if el.attrib.get("resource-id") == "com.dd.doordash:id/accessory":
                text = el.attrib.get("text", "").strip()
                if text:
                    opening_hours.append(text)
                    count += 1
                if count == 3:  # Stop after finding the first three
                    break

        if count == 3:
            break

    # Validate and return the results
    if len(opening_hours) < 3:
        # print("Failed to retrieve opening hours for three stores.")
        return False

    # print("Opening hours of the first three stores:", opening_hours)
    gt = f"Opening hours of the first three stores: {opening_hours}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
