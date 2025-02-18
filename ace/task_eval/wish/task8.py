from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Go to 'best sellers' in Wish app and then choose the first item. Finally go to 'related items'.",
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
    if len(history["actions"]) < 4:
        return False

    parser = ETParser(history["xml"][-4])
    best_element = parser.get_element("text", "Best sellers")

    if best_element is None:
        return False

    if history["actions"][-4]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(best_element)
    if clickable_parent is None:
        return False

    bounds = ETParser.get_bounds(clickable_parent)
    if (
        history["actions"][-4]["action"] != "tap"
        or history["actions"][-4]["x"] < bounds[0]
        or history["actions"][-4]["x"] > bounds[2]
        or history["actions"][-4]["y"] < bounds[1]
        or history["actions"][-4]["y"] > bounds[3]
    ):
        return False

    # click first item
    parser = ETParser(history["xml"][-3])
    list_element = parser.get_element_bydic(
        {"resource-id": "com.contextlogic.wish:id/recycler_2"}
    )

    if list_element is None:
        return False

    first_item = list_element.findall("*")[0]

    if first_item is None:
        return False

    if history["actions"][-3]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(first_item)
    if clickable_parent is None:
        return False

    bounds = ETParser.get_bounds(clickable_parent)
    if (
        history["actions"][-3]["action"] != "tap"
        or history["actions"][-3]["x"] < bounds[0]
        or history["actions"][-3]["x"] > bounds[2]
        or history["actions"][-3]["y"] < bounds[1]
        or history["actions"][-3]["y"] > bounds[3]
    ):
        return False

    # click related
    parser = ETParser(history["xml"][-2])
    related_element = parser.get_element("text", "Related")

    if related_element is None:
        return False

    if history["actions"][-2]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(related_element)
    if clickable_parent is None:
        return False

    bounds = ETParser.get_bounds(clickable_parent)
    if (
        history["actions"][-2]["x"] < bounds[0]
        or history["actions"][-2]["x"] > bounds[2]
        or history["actions"][-2]["y"] < bounds[1]
        or history["actions"][-2]["y"] > bounds[3]
    ):
        return False

    return True
