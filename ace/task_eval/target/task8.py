# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "After sorting by 'Best selling', retrieve the name and price of the first sausage in Target.",
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
    Evaluates the task of retrieving the name and price of the first sausage after sorting by 'Best selling'.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context (not used in this task).

    Returns:
        bool: True if the name and price are successfully retrieved, False otherwise.
    """
    # Step 1: Parse the XML to find the first product title
    parser = ETParser(xml)

    # Find the first product name using the specified resource-id
    product_name_element = parser.get_element(
        "resource-id", "com.target.ui:id/plp_v2_title"
    )
    if product_name_element is None:
        # print("Product name element not found.")
        return False

    # Extract the product name
    product_name = product_name_element.attrib.get("text", "").strip()
    if not product_name:
        # print("Product name text is missing.")
        return False

    # Step 2: Parse the XML to find the price of the product
    product_price_element = None
    for el in parser.et.iter():
        if el.attrib.get(
            "resource-id"
        ) == "com.target.ui:id/current_price" and el.attrib.get("content-desc"):
            product_price_element = el
            break

    if product_price_element is None:
        # print("Product price element not found.")
        return False

    # Extract the product price
    product_price = product_price_element.attrib.get("content-desc", "").strip()
    if not product_price:
        # print("Product price text is missing.")
        return False

    # Step 3: Print the extracted name and price
    gt = f"Product Name: {product_name} " + f"Product Price: {product_price}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
