# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "In Target, add the first 'sausage' into the cart and choose 'delivery' as soon as possible.",
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
    Evaluates the task of adding the first sausage to the cart and selecting delivery.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

            test action:{"action": "tap", "x": 396, "y": 1100},
                        {"action": "tap", "x": 381, "y": 1470},
                        {"action": "tap", "x": 500, "y": 2200},

    Returns:
        bool: True if the task was completed successfully, False otherwise.
    """

    # Step 1: Verify the "Add to Cart" button tap in xml[-4]
    try:
        add_to_cart_xml = ETParser(history["xml"][-4])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Add to Cart' action is missing.")
        return False

    add_to_cart_button = add_to_cart_xml.get_element(
        "resource-id", "com.target.ui:id/add_to_cart_button"
    )
    if add_to_cart_button is None:
        # print("'Add to Cart' button not found in xml[-4].")
        return False

    add_to_cart_bounds = add_to_cart_xml.get_bounds(add_to_cart_button)
    if add_to_cart_bounds is None:
        # print("Bounds for 'Add to Cart' button are missing.")
        return False

    try:
        add_to_cart_action = history["actions"][-4]
    except (KeyError, IndexError):
        # print("Previous action data for 'Add to Cart' is missing.")
        return False

    if not (
        add_to_cart_bounds[0] <= add_to_cart_action["x"] <= add_to_cart_bounds[2]
        and add_to_cart_bounds[1] <= add_to_cart_action["y"] <= add_to_cart_bounds[3]
    ):
        # print("The action for 'Add to Cart' was not within the expected bounds.")
        return False

    # Step 2: Verify the "Delivery" selection in xml[-3]
    try:
        delivery_xml = ETParser(history["xml"][-3])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Delivery' selection is missing.")
        return False

    delivery_element = delivery_xml.get_element("text", "Delivery")
    if delivery_element is None:
        # print("Delivery option not found in xml[-3].")
        return False

    # Find the parent element of the delivery option
    parent_element = delivery_xml.find_parent(delivery_element)
    if parent_element is None:
        # print("Parent element for 'Delivery' option not found.")
        return False

    delivery_bounds = delivery_xml.get_bounds(parent_element)
    if delivery_bounds is None:
        # print("Bounds for 'Delivery' option parent are missing.")
        return False

    try:
        delivery_action = history["actions"][-3]
    except (KeyError, IndexError):
        # print("Previous action data for 'Delivery' selection is missing.")
        return False

    if not (
        delivery_bounds[0] <= delivery_action["x"] <= delivery_bounds[2]
        and delivery_bounds[1] <= delivery_action["y"] <= delivery_bounds[3]
    ):
        # print("The action for 'Delivery' was not within the expected bounds.")
        return False

    # Step 3: Verify the final "Add to Cart" button tap in xml[-2]
    try:
        final_add_to_cart_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Previous XML data for final 'Add to Cart' action is missing.")
        return False

    final_add_to_cart_button = final_add_to_cart_xml.get_element(
        "resource-id", "com.target.ui:id/add_to_cart_button"
    )
    if final_add_to_cart_button is None:
        # print("Final 'Add to Cart' button not found in xml[-2].")
        return False

    final_add_to_cart_bounds = final_add_to_cart_xml.get_bounds(
        final_add_to_cart_button
    )
    if final_add_to_cart_bounds is None:
        # print("Bounds for final 'Add to Cart' button are missing.")
        return False

    try:
        final_add_to_cart_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data for final 'Add to Cart' is missing.")
        return False

    if not (
        final_add_to_cart_bounds[0]
        <= final_add_to_cart_action["x"]
        <= final_add_to_cart_bounds[2]
        and final_add_to_cart_bounds[1]
        <= final_add_to_cart_action["y"]
        <= final_add_to_cart_bounds[3]
    ):
        # print("The action for final 'Add to Cart' was not within the expected bounds.")
        return False

    # print("Successfully added the first sausage to the cart and selected delivery.")
    return True
