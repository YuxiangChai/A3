# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "View badges in Fitbit for tracking achievements.",
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
    Validates whether the required badge categories are present in Fitbit.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context, including XML and actions.

    Returns:
        bool: True if all required badge categories are present, False otherwise.
    """
    # Parse the XML
    parser = ETParser(xml)

    # Flags for each required badge category
    found_daily_steps = False
    found_lifetime_distance = False
    found_weight_goal = False

    # Search for the required text labels
    for el in parser.et.iter():
        text = el.attrib.get("text", "")
        if text == "Daily steps":
            found_daily_steps = True
        elif text == "Lifetime distance":
            found_lifetime_distance = True
        elif text == "Weight goal":
            found_weight_goal = True

    # Check if all categories are found
    return found_daily_steps and found_lifetime_distance and found_weight_goal
