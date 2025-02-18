# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "View lyrics on the playback screen in Youtube Music.",
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
    Evaluates whether the Lyrics screen was successfully opened.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the Lyrics screen was opened, False otherwise.
    """
    # Step 1: Ensure sufficient history is available
    if len(history["actions"]) < 2 or len(history["xml"]) < 2:
        # print("Insufficient history for validation.")
        return False

    # Step 2: Parse xml[-2] to find the "Lyrics" button and get its bounds
    previous_xml = history["xml"][-2]
    parser = ETParser(previous_xml)
    lyrics_button = parser.get_element("content-desc", "Lyrics")

    if not lyrics_button:
        # print("Lyrics button not found in the previous XML.")
        return False

    # Extract bounds from the "Lyrics" button
    bounds_str = lyrics_button.attrib.get("bounds", "")
    if not bounds_str:
        # print("Bounds attribute not found for 'Lyrics' button.")
        return False

    # Parse bounds into coordinates
    try:
        bounds = bounds_str.strip("[]").split("][")
        x1, y1 = map(int, bounds[0].split(","))
        x2, y2 = map(int, bounds[1].split(","))
    except ValueError:
        # print("Failed to parse bounds for 'Lyrics' button.")
        return False

    # Step 3: Validate action[-2] against the "Lyrics" button bounds
    last_action = history["actions"][-2]
    if last_action["action"] != "tap" or not (
        x1 <= last_action["x"] <= x2 and y1 <= last_action["y"] <= y2
    ):
        # print("The last action was not within the 'Lyrics' button bounds.")
        return False

    # Step 4: Check if the latest xml contains a selected "Lyrics" tab
    current_xml = history["xml"][-1]
    parser = ETParser(current_xml)
    lyrics_tab = parser.get_element_bydic(
        {"content-desc": "Lyrics", "selected": "true"}
    )

    if lyrics_tab:
        # print("Lyrics screen is open.")
        return True
    else:
        # print("Lyrics screen not detected.")
        return False
