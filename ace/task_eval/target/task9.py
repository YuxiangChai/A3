# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Retrieve the subtotal and item count from the Cart in Target shopping cart page.",
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
    Evaluates the task of retrieving the subtotal and item count from the Cart.

    Args:
        xml (str): XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context (not used in this task).

    Returns:
        bool: True if the subtotal and item count are successfully retrieved, False otherwise.
    """
    # Step 1: Locate the parent node with resource-id="com.target.ui:id/composable_toolbar"
    parser = ETParser(xml)
    toolbar_element = parser.get_element(
        "resource-id", "com.target.ui:id/composable_toolbar"
    )

    if toolbar_element is None:
        # print(
        #     "Parent element with resource-id 'com.target.ui:id/composable_toolbar' not found."
        # )
        return False

    # Step 2: Traverse its child elements to find the desired text
    extracted_info = []
    for child in toolbar_element.iter():
        text = child.attrib.get("text", "").strip()
        if text:  # If the child element has a non-empty text attribute
            extracted_info.append(text)

    if not extracted_info:
        # print("No text information found under the parent element.")
        return False

    # Step 3: Check if the desired text is present
    for info in extracted_info:
        if "subtotal" in info and "items" in info:
            gt = f"Cart Infomation: {info}"
            judge = answer_correct_judge(
                task,
                answer,
                gt,
                client,
                model_type,
            )
            return judge

    # print("Desired information about subtotal and item count not found.")
    return False
