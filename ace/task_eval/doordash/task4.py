# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Add a hash brown to the cart in the McDonald's store on DoorDash, then open the cart to verify it was added successfully.",
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
    Validates whether the user has successfully added a hash brown to the cart
    and opened the cart on DoorDash.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the cart contains "Hash Browns" and was opened correctly, False otherwise.
    """
    # Step 1: Validate the "Order Cart" button tap
    try:
        order_cart_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Order Cart' is missing.")
        return False

    # Locate the "Order Cart" button
    order_cart_element = None
    for el in order_cart_xml.et.iter():
        if el.attrib.get("resource-id") == "com.dd.doordash:id/button_orderCart":
            order_cart_element = el
            break

    if order_cart_element is None:
        # print("Order Cart button not found in xml[-2].")
        return False

    # Extract and parse the bounds of the "Order Cart" button
    cart_bounds_str = order_cart_element.attrib.get("bounds", "")
    cart_bounds_values = cart_bounds_str.strip("[]").split("][")
    cart_x1, cart_y1 = map(int, cart_bounds_values[0].split(","))
    cart_x2, cart_y2 = map(int, cart_bounds_values[1].split(","))

    # Validate the tap action on the "Order Cart" button
    try:
        cart_open_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data for opening the cart is missing.")
        return False

    if not (
        cart_x1 <= cart_open_action["x"] <= cart_x2
        and cart_y1 <= cart_open_action["y"] <= cart_y2
    ):
        # print("The action for opening the cart was not within the expected bounds.")
        return False

    # Step 2: Check if the cart contains "Hash Browns"
    parser_title = ETParser(xml)
    hash_brown_element = None

    for el in parser_title.et.iter():
        if el.attrib.get("resource-id") == "com.dd.doordash:id/cartItemNameTextView":
            hash_brown_element = el
            break

    # Validate if the element contains "Hash Browns"
    if hash_brown_element is not None:
        if hash_brown_element.attrib.get("text") == "Hash Browns":
            # print("Hash Browns successfully added to the cart.")
            return True
        else:
            # print("The item in the cart is not 'Hash Browns'.")
            return False
    else:
        # print("No item found in the cart.")
        return False
