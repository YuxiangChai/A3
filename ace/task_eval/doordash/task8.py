# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "Let me know the items in my shopping cart on Doordash.",
        "level": "easy",
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
    Extracts and displays the items in the shopping cart based on the XML data.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string.
        history (list[dict]): List containing historical context (not used here).

    Returns:
        bool: True if items were successfully extracted and displayed, False otherwise.
    """
    # Initialize the XML parser
    parser = ETParser(xml)

    # Define the XPath for locating shopping cart items
    xpath = ".//*[@resource-id='com.dd.doordash:id/store_item_names']"

    # Get all elements matching the XPath
    elements = parser.get_elements(xpath)

    if not elements:
        # print("No items found in the shopping cart.")
        return False

    # Extract the text content of all matching elements
    item_texts = [
        el.attrib.get("text", "").strip() for el in elements if "text" in el.attrib
    ]

    # Combine the extracted text into a comma-separated string
    shopping_cart_items = ", ".join(item_texts)

    # Display the extracted items
    # print("Shopping Cart Items:", shopping_cart_items)
    gt = f"Shopping Cart Items: {shopping_cart_items}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
