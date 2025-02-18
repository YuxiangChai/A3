# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "In Target, remove all items from the Delivery section of the shopping cart.",
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
    Evaluates whether all items were successfully removed from the Delivery section of the shopping cart.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if all items were successfully removed, False otherwise.
    """

    # Step 1: Validate tap on "Edit" button in the Delivery section (xml[-4])
    try:
        edit_button_xml = ETParser(history["xml"][-4])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Edit' action is missing.")
        return False

    edit_button_element = edit_button_xml.get_element(
        "resource-id", "com.target.ui:id/fulfillment_header_edit_button"
    )
    if edit_button_element is None:
        # print("Edit button in the Delivery section not found.")
        return False

    edit_button_bounds = edit_button_xml.get_bounds(edit_button_element)
    if edit_button_bounds is None:
        # print("Bounds for 'Edit' button are missing.")
        return False

    try:
        edit_action = history["actions"][-4]
    except (KeyError, IndexError):
        # print("Previous action data for 'Edit' button is missing.")
        return False

    if not (
        edit_button_bounds[0] <= edit_action["x"] <= edit_button_bounds[2]
        and edit_button_bounds[1] <= edit_action["y"] <= edit_button_bounds[3]
    ):
        # print("The action for 'Edit' was not within the expected bounds.")
        return False

    # Step 2: Validate tap on "Remove items" button (xml[-3])
    try:
        remove_items_xml = ETParser(history["xml"][-3])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Remove items' action is missing.")
        return False

    remove_items_element = remove_items_xml.get_element("text", "Remove items")
    if remove_items_element is None:
        # print("'Remove items' button not found.")
        return False

    remove_items_bounds = remove_items_xml.get_bounds(remove_items_element)
    if remove_items_bounds is None:
        # print("Bounds for 'Remove items' button are missing.")
        return False

    try:
        remove_items_action = history["actions"][-3]
    except (KeyError, IndexError):
        # print("Previous action data for 'Remove items' button is missing.")
        return False

    if not (
        remove_items_bounds[0] <= remove_items_action["x"] <= remove_items_bounds[2]
        and remove_items_bounds[1] <= remove_items_action["y"] <= remove_items_bounds[3]
    ):
        # print("The action for 'Remove items' was not within the expected bounds.")
        return False

    # Step 3: Validate tap on confirmation "Go ahead" button (xml[-2])
    try:
        confirmation_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Previous XML data for confirmation action is missing.")
        return False

    confirmation_element = confirmation_xml.get_element(
        "resource-id", "com.target.ui:id/checkout_confirmation_go_ahead_button"
    )
    if confirmation_element is None:
        # print("Confirmation 'Go ahead' button not found.")
        return False

    confirmation_bounds = confirmation_xml.get_bounds(confirmation_element)
    if confirmation_bounds is None:
        # print("Bounds for confirmation 'Go ahead' button are missing.")
        return False

    try:
        confirmation_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data for confirmation button is missing.")
        return False

    if not (
        confirmation_bounds[0] <= confirmation_action["x"] <= confirmation_bounds[2]
        and confirmation_bounds[1] <= confirmation_action["y"] <= confirmation_bounds[3]
    ):
        # print("The action for confirmation was not within the expected bounds.")
        return False

    # print("Successfully removed all items from the Delivery section.")
    return True
