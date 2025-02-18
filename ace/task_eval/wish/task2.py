from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open Wish app and search for 'flashlight' and set filter to under 100",
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
    parser = ETParser(xml)
    search_element = parser.get_element(
        "resource-id", "com.contextlogic.wish:id/home_page_search_text"
    )

    if search_element is not None:
        if search_element.attrib["text"].lower() != "flashlight":
            return False

    under100_element = parser.get_element_bydic(
        {"resource-id": "com.contextlogic.wish:id/title", "text": "Under 100"}
    )

    if under100_element is None:
        return False

    for action_step in range(len(history["actions"]) - 2, -1, -1):
        # if tap_completed == tap_task:
        #     return True
        if history["actions"][action_step]["action"] == "tap":
            parser = ETParser(history["xml"][action_step])
            clickable_parent = parser.find_clickable_parent(under100_element)
            if clickable_parent is None:
                return False

            bounds = ETParser.get_bounds(clickable_parent)
            if (
                history["actions"][action_step]["action"] == "tap"
                and history["actions"][action_step]["x"] > bounds[0]
                and history["actions"][action_step]["x"] < bounds[2]
                and history["actions"][action_step]["y"] > bounds[1]
                and history["actions"][action_step]["y"] < bounds[3]
            ):
                return True

    return False
