# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Sorting the results by 'Best selling' after searching 'sausage' in Target.",
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
    Evaluates the task of sorting results by 'Best selling' on Target.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if the task was completed successfully, False otherwise.
    """

    # Step 1: Validate tap on "Sort by" button in xml[-4]
    try:
        sort_by_xml = ETParser(history["xml"][-4])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Sort by' selection is missing.")
        return False

    sort_by_element = sort_by_xml.get_element("content-desc", "sort by")
    if sort_by_element is None:
        # print("The 'Sort by' button was not found in xml[-4].")
        return False

    sort_by_bounds = sort_by_xml.get_bounds(sort_by_element)
    if sort_by_bounds is None:
        # print("Bounds for 'Sort by' button are missing.")
        return False

    try:
        sort_by_action = history["actions"][-4]
    except (KeyError, IndexError):
        # print("Previous action data for 'Sort by' selection is missing.")
        return False

    if not (
        sort_by_bounds[0] <= sort_by_action["x"] <= sort_by_bounds[2]
        and sort_by_bounds[1] <= sort_by_action["y"] <= sort_by_bounds[3]
    ):
        # print("The action for selecting 'Sort by' was not within the expected bounds.")
        return False

    # Step 2: Validate tap on "Best selling" option in xml[-3]
    try:
        best_selling_xml = ETParser(history["xml"][-3])
    except (KeyError, IndexError):
        # print("Previous XML data for 'Best selling' selection is missing.")
        return False

    best_selling_element = best_selling_xml.get_element("text", "Best selling")
    if best_selling_element is None:
        # print("'Best selling' option was not found in xml[-3].")
        return False

    best_selling_bounds = best_selling_xml.get_bounds(best_selling_element)
    if best_selling_bounds is None:
        # print("Bounds for 'Best selling' option are missing.")
        return False

    try:
        best_selling_action = history["actions"][-3]
    except (KeyError, IndexError):
        # print("Previous action data for 'Best selling' selection is missing.")
        return False

    if not (
        best_selling_bounds[0] <= best_selling_action["x"] <= best_selling_bounds[2]
        and best_selling_bounds[1] <= best_selling_action["y"] <= best_selling_bounds[3]
    ):
        # print(
        #     "The action for selecting 'Best selling' was not within the expected bounds."
        # )
        return False

    # Step 3: Validate tap on "See results" button in xml[-2]
    try:
        see_results_xml = ETParser(history["xml"][-2])
    except (KeyError, IndexError):
        # print("Previous XML data for 'See results' selection is missing.")
        return False

    see_results_element = see_results_xml.get_element("content-desc", "See results")
    if see_results_element is None:
        # print("The 'See results' button was not found in xml[-2].")
        return False

    see_results_bounds = see_results_xml.get_bounds(see_results_element)
    if see_results_bounds is None:
        # print("Bounds for 'See results' button are missing.")
        return False

    try:
        see_results_action = history["actions"][-2]
    except (KeyError, IndexError):
        # print("Previous action data for 'See results' selection is missing.")
        return False

    if not (
        see_results_bounds[0] <= see_results_action["x"] <= see_results_bounds[2]
        and see_results_bounds[1] <= see_results_action["y"] <= see_results_bounds[3]
    ):
        # print(
        #     "The action for selecting 'See results' was not within the expected bounds."
        # )
        return False

    # Step 4: Validate the final XML contains the sorted results
    # parser = ETParser(xml)
    # sorted_result_element = parser.get_element("text", "Best selling")
    # if sorted_result_element is None:
    #     print("The sorted results by 'Best selling' were not found in the final XML.")
    #     return False

    # print("Successfully sorted the results by 'Best selling'.")
    return True
