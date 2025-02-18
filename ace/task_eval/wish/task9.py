from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Navigate to 'best sellers' on Wish app and choose the first item.",
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

    for j, xml in enumerate(history["xml"]):
        parser = ETParser(xml)
        best_element = parser.get_element("text", "Best sellers")
        if best_element is not None:
            i = j
            break

    if best_element is None:
        return False

    clickable_parent = parser.find_clickable_parent(best_element)
    if clickable_parent is None:
        return False

    bounds = ETParser.get_bounds(clickable_parent)
    if (
        history["actions"][i]["action"] != "tap"
        or history["actions"][i]["x"] < bounds[0]
        or history["actions"][i]["x"] > bounds[2]
        or history["actions"][i]["y"] < bounds[1]
        or history["actions"][i]["y"] > bounds[3]
    ):
        return False

    # click first item
    parser = ETParser(history["xml"][i + 1])
    list_element = parser.get_element_bydic(
        {"resource-id": "com.contextlogic.wish:id/recycler_2"}
    )

    if list_element is None:
        return False

    first_item = list_element.findall("*")[0]

    if first_item is None:
        return False

    if history["actions"][i + 1]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(first_item)
    if clickable_parent is None:
        return False

    bounds = ETParser.get_bounds(clickable_parent)
    if (
        history["actions"][i + 1]["action"] != "tap"
        or history["actions"][i + 1]["x"] < bounds[0]
        or history["actions"][i + 1]["x"] > bounds[2]
        or history["actions"][i + 1]["y"] < bounds[1]
        or history["actions"][i + 1]["y"] > bounds[3]
    ):
        return False

    return True
