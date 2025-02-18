# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open the comments section in a YouTube Shorts video and like the first comment.",
        "level": "medium",
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
    Evaluates whether the task of liking the first comment in the YouTube Shorts comments section is successfully completed.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the task is successfully completed, False otherwise.
    """

    # Step 1: Validate that the actions were performed in the Comments section
    for idx in [-1, -2]:
        parser = ETParser(history["xml"][idx])

        comments_element = parser.get_element(
            "resource-id", "com.google.android.youtube:id/modern_title"
        )
        if (
            comments_element is None
            or comments_element.attrib.get("text", "").strip() != "Comments"
        ):
            # print(f"XML index {idx}: Not in the Comments section.")
            return False

    # print("Validated: Actions occurred in the Comments section.")

    # Step 2: Validate the tap action on the Like button
    parser = ETParser(history["xml"][-2])

    # Find the first "Like this comment..." element
    like_elements = []
    for el in parser.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if content_desc.startswith("Like this comment"):
            like_elements.append(el)

    if len(like_elements) < 1:
        # print("No 'Like this comment' element found in XML index -2.")
        return False

    # Get the first Like button's bounds
    first_like_element = like_elements[0]
    like_button_child = next(
        iter(first_like_element), None
    )  # Get the first child element
    if like_button_child is None:
        # print("No child element found for the first 'Like this comment' element.")
        return False

    like_bounds = like_button_child.attrib.get("bounds", "")
    if not like_bounds:
        # print("Bounds for the Like button are missing.")
        return False

    # Parse bounds
    like_coords = like_bounds.strip("[]").split("][")
    like_x1, like_y1 = map(int, like_coords[0].split(","))
    like_x2, like_y2 = map(int, like_coords[1].split(","))

    # Validate the tap action
    like_action = history["actions"][-2]
    if like_action["action"] != "tap":
        # print("Action -2 is not a tap.")
        return False

    if not (
        like_x1 <= like_action["x"] <= like_x2
        and like_y1 <= like_action["y"] <= like_y2
    ):
        # print("Action -2 did not occur within the Like button bounds.")
        return False

    # print("Validated: Like button was tapped correctly.")

    # Step 3: Validate the Like button state in the final XML
    parser = ETParser(history["xml"][-1])
    unlike_element = parser.get_element("content-desc", "Unlike")
    if unlike_element is not None:
        # print("Like button is in the 'liked' state.")
        return True

    # print("Like button is not in the 'liked' state.")
    return False
