# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task description.
    """
    return {
        "task": "Retrieve the names of the first three stores in the 'Shopping' section in DoorDash.",
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
    Extracts the names of the first three stores in the 'Shopping' section from DoorDash.

    Args:
        xml (str): XML content as a string (not used here).
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context containing XMLs.

    Returns:
        list[str]: A list containing the names of the first three stores, or an empty list if not found.
    """
    # Initialize list to store store names
    store_names = []

    # Step 1: Iterate over all XMLs in history
    for idx, xml_data in enumerate(history["xml"]):
        parser = ETParser(xml_data)

        text_list = []

        # Traverse all elements in the XML
        for element in parser.et.iter():
            # Check for elements with the resource-id="com.dd.doordash:id/title"
            if element.attrib.get("resource-id") == "com.dd.doordash:id/title":
                text_value = element.attrib.get("text", "").strip()
                text_list.append(text_value)

        # Validate if the first text is "Shopping"
        if len(text_list) > 0 and text_list[0] == "Shopping":
            # Extract the first three store names
            store_names = text_list[1:4]  # Get the second, third, and fourth elements
            gt = f"Store names: {store_names}"
            # print(f"Found Shopping section in XML index {idx}. Store names: {store_names}")
            break

    if store_names == []:
        # print("No valid Shopping section found in the provided XML history.")
        return False

    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
