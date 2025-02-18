# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    Note:
    1. The config file must set `screenshoting` to `false` to avoid capturing screenshots.
    2. The `eval` and `get_state` functions in `avd_control.py` have been modified to include the option
       to disable screenshot capturing through parameters.
    3. Example usage:
       - To disable both XML and screenshot capturing in `get_state`:
         state = controller.get_state(include_xml=False, include_screenshot=False)
       - To disable screenshot capturing in `eval`:
         eval_result = controller.eval(include_screenshot=False)
    """
    return {
        "task": "Display the barcode in the wallet section for checkout in Target.",
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
    Evaluates whether the user successfully displayed the barcode in the wallet section.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the barcode is successfully displayed, False otherwise.
    """

    # Step 1: Validate tap on "Show my barcode" button in xml[-2]
    try:
        barcode_button_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Show my barcode' action is missing.")
        return False

    barcode_button_element = barcode_button_xml.get_element("text", "Show my barcode")
    if barcode_button_element is None:
        # print("'Show my barcode' button not found in xml[-2].")
        return False

    barcode_button_bounds = barcode_button_xml.get_bounds(barcode_button_element)
    if barcode_button_bounds is None:
        # print("Bounds for 'Show my barcode' button are missing.")
        return False

    try:
        barcode_button_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data for 'Show my barcode' button is missing.")
        return False

    if not (
        barcode_button_bounds[0]
        <= barcode_button_action["x"]
        <= barcode_button_bounds[2]
        and barcode_button_bounds[1]
        <= barcode_button_action["y"]
        <= barcode_button_bounds[3]
    ):
        # print("The action for 'Show my barcode' was not within the expected bounds.")
        return False

    # Step 2: Validate the barcode text in xml[-1]
    try:
        barcode_xml = ETParser(history["xml"][-1])
    except (KeyError, IndexError):
        # print("Previous XML data for the barcode display is missing.")
        return False

    barcode_text_element = barcode_xml.get_element(
        "text", "Show at checkout or scan with hand scanner"
    )
    if barcode_text_element is None:
        # print("'Show at checkout or scan with hand scanner' text not found in xml[-1].")
        return False

    # print("Successfully displayed the barcode in the wallet section.")
    return True
