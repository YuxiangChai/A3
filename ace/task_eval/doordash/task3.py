# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the alcohol section in DoorDash.",
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
    Validates whether the user has successfully opened the Alcohol section in DoorDash.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the Alcohol section is open, False otherwise.
    """
    # Step 1: Validate the tap on the "Alcohol" element in xml[-2]
    try:
        alcohol_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Alcohol' selection is missing.")
        return False

    # Locate the "Alcohol" element
    alcohol_element = None
    for el in alcohol_xml.et.iter():
        if el.attrib.get("text") == "Alcohol":
            alcohol_element = el
            break

    if alcohol_element is None:
        # print("Alcohol element not found in xml[-2].")
        return False

    # Extract and parse the bounds of the "Alcohol" element
    bounds_str = alcohol_element.attrib.get("bounds", "")
    bounds_values = bounds_str.strip("[]").split("][")
    x1, y1 = map(int, bounds_values[0].split(","))
    x2, y2 = map(int, bounds_values[1].split(","))

    # Validate the tap action on the "Alcohol" element
    try:
        alcohol_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data for 'Alcohol' selection is missing.")
        return False

    if not (x1 <= alcohol_action["x"] <= x2 and y1 <= alcohol_action["y"] <= y2):
        # print("The action for selecting 'Alcohol' was not within the expected bounds.")
        return False

    # Step 2: Validate the presence of the "Alcohol" title in xml[-1]
    parser_title = ETParser(xml)
    title_element = None
    for el in parser_title.et.iter():
        if (
            el.attrib.get("resource-id")
            == "com.dd.doordash:id/textView_navBar_backdropTitle"
        ):
            title_element = el
            break

    # Check if the title element matches "Alcohol"
    if title_element is not None:
        if title_element.attrib.get("text") == "Alcohol":
            # print("Successfully navigated to the Alcohol section.")
            return True
        else:
            # print(
            #     f"Current section is: {title_element.attrib.get('text')}. Expected: 'Alcohol'."
            # )
            return False
    else:
        # print("Alcohol title element not found in xml[-1].")
        return False
