# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Filter results to show restaurants with a rating of 4.8 or above after searching 'hot dog' on DoorDash.",
        "level": "hard",
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
    Validates the filtering process for restaurants with a rating of 4.8 or above on DoorDash.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the filtering process was successfully completed, False otherwise.
    """

    # Step 1: Validate tap on the "Ratings" button in xml[-4]
    try:
        ratings_xml = ETParser(history["xml"][-4])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Ratings' selection is missing.")
        return False

    ratings_element = None
    for el in ratings_xml.et.iter():
        if el.attrib.get("text") == "Ratings":
            ratings_element = el
            break

    if ratings_element is None:
        # print("Ratings button not found in xml[-4].")
        return False

    bounds_str = ratings_element.attrib.get("bounds", "")
    bounds_values = bounds_str.strip("[]").split("][")
    r_x1, r_y1 = map(int, bounds_values[0].split(","))
    r_x2, r_y2 = map(int, bounds_values[1].split(","))

    try:
        ratings_action = history["actions"][-4]
    except (KeyError, IndexError):
        # print("Previous action data for 'Ratings' selection is missing.")
        return False

    if not (
        r_x1 <= ratings_action["x"] <= r_x2 and r_y1 <= ratings_action["y"] <= r_y2
    ):
        # print("The action for selecting 'Ratings' was not within the expected bounds.")
        return False

    # Step 2: Validate tap on the "4.8" rating in xml[-3]
    try:
        ratings_xml3 = ETParser(history["xml"][-3])
    except (KeyError, IndexError):
        # print("Previous XML data for rating '4.8' selection is missing.")
        return False

    seekbar_element = None
    rating_text_element = None
    for el in ratings_xml3.et.iter():
        if el.attrib.get("resource-id") == "com.dd.doordash:id/seekBar":
            seekbar_element = el
        elif el.attrib.get("text") == "4.8":
            rating_text_element = el
        if seekbar_element and rating_text_element:
            break

    if seekbar_element is None or rating_text_element is None:
        # print("SeekBar or '4.8' element not found in xml[-3].")
        return False

    seekbar_bounds = seekbar_element.attrib.get("bounds", "")
    seekbar_values = seekbar_bounds.strip("[]").split("][")
    s_y1 = int(seekbar_values[0].split(",")[1])
    s_y2 = int(seekbar_values[1].split(",")[1])

    rating_bounds = rating_text_element.attrib.get("bounds", "")
    rating_values = rating_bounds.strip("[]").split("][")
    r_x1 = int(rating_values[0].split(",")[0])
    r_x2 = int(rating_values[1].split(",")[0])

    try:
        rating_action = history["actions"][-3]
    except (KeyError, IndexError):
        # print("Previous action data for rating '4.8' selection is missing.")
        return False

    if not (r_x1 <= rating_action["x"] <= r_x2 and s_y1 <= rating_action["y"] <= s_y2):
        # print("The action for selecting 4.8 rating was not within the expected bounds.")
        return False

    # Step 3: Validate tap on the "View Results" button in xml[-2]
    try:
        results_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Previous XML data for 'View Results' selection is missing.")
        return False

    view_results_element = None
    for el in results_xml.et.iter():
        if el.attrib.get("resource-id") == "com.dd.doordash:id/view_results":
            view_results_element = el
            break

    if view_results_element is None:
        # print("View Results button not found in xml[-2].")
        return False

    view_results_bounds_str = view_results_element.attrib.get("bounds", "")
    view_results_bounds = view_results_bounds_str.strip("[]").split("][")
    vr_x1, vr_y1 = map(int, view_results_bounds[0].split(","))
    vr_x2, vr_y2 = map(int, view_results_bounds[1].split(","))

    try:
        view_results_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data for 'View Results' selection is missing.")
        return False

    if not (
        vr_x1 <= view_results_action["x"] <= vr_x2
        and vr_y1 <= view_results_action["y"] <= vr_y2
    ):
        # print("The action for selecting 'View Results' was not within the expected bounds.")
        return False

    # Step 4: Validate result in the latest XML
    parser = ETParser(xml)
    result_element = None
    for el in parser.et.iter():
        if el.attrib.get("text") == "Over 4.8":
            result_element = el
            break

    if result_element is None:
        # print("Filtered results with 'Over 4.8' not found in the latest XML.")
        return False

    # print("Successfully filtered results for restaurants with a rating of 4.8 or above.")
    return True
