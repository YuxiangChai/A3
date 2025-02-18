# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "in Target, switch from the Discover page to the Cart.",
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
    Evaluates whether the user successfully switched from the Discover page to the Cart.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the Cart is successfully selected, False otherwise.
    """

    # Step 1: Parse the XML to find the unique element with resource-id="com.target.ui:id/largeLabel" and text="Cart"
    parser = ETParser(xml)
    cart_element = parser.get_element_bydic(
        {"resource-id": "com.target.ui:id/largeLabel", "text": "Cart"}
    )

    if cart_element is None:
        # print("Cart element with specified attributes not found in the XML.")
        return False

    # Step 2: Check if the 'selected' attribute of the Cart element is "true"
    is_selected = cart_element.attrib.get("selected", "").lower()
    if is_selected == "true":
        # print("The Cart is successfully selected.")
        return True
    else:
        # print("The Cart is not selected.")
        return False
