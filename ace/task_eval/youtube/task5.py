# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Select the “Shorts” tab in YouTube and like the first video.",
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
    Evaluates whether the user successfully selected the "Shorts" tab in YouTube
    and liked the first video.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context with XMLs and actions.

    Returns:
        bool: True if the task is successfully completed, False otherwise.
    """

    if len(history["actions"]) < 3:
        print("Not enough actions in history.")
        return False

    # Step 1: Check if the third last action clicked the Shorts region
    parser = ETParser(history["xml"][-3])
    shorts_element = parser.get_element("content-desc", "Shorts")
    if shorts_element is None:
        # print("Shorts element not found in history XML [-3].")
        return False

    shorts_bounds = shorts_element.attrib.get("bounds", "")
    if not shorts_bounds:
        # print("Bounds for Shorts element are missing.")
        return False

    # Parse Shorts bounds
    shorts_coords = shorts_bounds.strip("[]").split("][")
    shorts_x1, shorts_y1 = map(int, shorts_coords[0].split(","))
    shorts_x2, shorts_y2 = map(int, shorts_coords[1].split(","))

    shorts_action = history["actions"][-3]
    if not (
        shorts_x1 <= shorts_action["x"] <= shorts_x2
        and shorts_y1 <= shorts_action["y"] <= shorts_y2
    ):
        # print("The third last action was not within the Shorts region.")
        return False

    # Step 2: Check if the second last action clicked the Like region
    parser = ETParser(history["xml"][-2])
    like_element = None

    # Search for an element with content-desc starting with "like this video"
    for el in parser.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if content_desc.startswith("like this video"):
            like_element = el
            break

    if like_element is None:
        # print("Like button element not found in history XML [-2].")
        return False

    like_bounds = like_element.attrib.get("bounds", "")
    if not like_bounds:
        # print("Bounds for Like button are missing.")
        return False

    # Parse Like bounds
    like_coords = like_bounds.strip("[]").split("][")
    like_x1, like_y1 = map(int, like_coords[0].split(","))
    like_x2, like_y2 = map(int, like_coords[1].split(","))

    like_action = history["actions"][-2]
    if not (
        like_x1 <= like_action["x"] <= like_x2
        and like_y1 <= like_action["y"] <= like_y2
    ):
        # print("The second last action was not within the Like region.")
        return False

    # Step 3: Confirm the Like button state in the current XML
    parser = ETParser(xml)
    like_state_element = parser.get_element("content-desc", "unlike")
    if like_state_element is not None:
        # print("Like button is in the 'liked' state.")
        return True

    # print("Like button not found in the final state or it is not in liked state.")
    return False
