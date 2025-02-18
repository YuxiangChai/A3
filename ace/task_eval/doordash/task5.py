# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Remove the first item from the cart in DoorDash.",
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
    Validates that the user has correctly removed the first item from the cart in DoorDash.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used in this task).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if the action was completed successfully, False otherwise.
    """
    # Step 1: Check if the "trashbin" button was tapped in the cart XML
    cart_xml = ETParser(history["xml"][-3])
    trashbin_button_element = None
    for el in cart_xml.et.iter():
        if el.attrib.get("resource-id") == "com.dd.doordash:id/store_delete_icon":
            trashbin_button_element = el
            break

    if trashbin_button_element is None:
        # print("Trashbin button not found in xml[-3].")
        return False

    # Extract and parse the bounds of the trashbin button
    trashbin_button_bounds_str = trashbin_button_element.attrib.get("bounds", "")
    trashbin_bounds_values = trashbin_button_bounds_str.strip("[]").split("][")
    trashbin_x1, trashbin_y1 = map(int, trashbin_bounds_values[0].split(","))
    trashbin_x2, trashbin_y2 = map(int, trashbin_bounds_values[1].split(","))

    # Validate the tap action on the trashbin button
    delete_action = history["actions"][-3]
    if not (
        trashbin_x1 <= delete_action["x"] <= trashbin_x2
        and trashbin_y1 <= delete_action["y"] <= trashbin_y2
    ):
        # print("The action for deleting the order was not within the expected bounds.")
        return False

    # Step 2: Check if the "Yes, delete" confirm button was tapped
    confirm_xml = ETParser(history["xml"][-2])
    confirm_element = None
    for el in confirm_xml.et.iter():
        if el.attrib.get("text") == "Yes, delete":
            confirm_element = el
            break

    if confirm_element is None:
        # print("Confirm button not found in xml[-2].")
        return False

    # Extract and parse the bounds of the confirm button
    confirm_button_bounds_str = confirm_element.attrib.get("bounds", "")
    confirm_bounds_values = confirm_button_bounds_str.strip("[]").split("][")
    confirm_x1, confirm_y1 = map(int, confirm_bounds_values[0].split(","))
    confirm_x2, confirm_y2 = map(int, confirm_bounds_values[1].split(","))

    # Validate the tap action on the confirm button
    confirm_action = history["actions"][-2]
    if not (
        confirm_x1 <= confirm_action["x"] <= confirm_x2
        and confirm_y1 <= confirm_action["y"] <= confirm_y2
    ):
        # print(
        #     "The action for confirming 'deleting the order' was not within the expected bounds."
        # )
        return False

    # If all checks pass, return True
    return True
