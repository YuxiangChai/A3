from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search for 'bottle' in the Wish app and set filter to under 100. Then choose the first item and add it to wistlist",
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
    if len(history["actions"]) < 5:
        return False

    parser = ETParser(history["xml"][-5])
    search_element = parser.get_element(
        "resource-id", "com.contextlogic.wish:id/home_page_search_text"
    )

    if search_element is None:
        return False

    if search_element.attrib["text"].lower() != "bottle":
        return False

    under100_element = parser.get_element_bydic(
        {"resource-id": "com.contextlogic.wish:id/title", "text": "Under 100"}
    )

    if under100_element is None:
        return False

    if history["actions"][-5]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(under100_element)
    if clickable_parent is None:
        return False

    bounds = ETParser.get_bounds(clickable_parent)
    if (
        history["actions"][-5]["action"] != "tap"
        or history["actions"][-5]["x"] < bounds[0]
        or history["actions"][-5]["x"] > bounds[2]
        or history["actions"][-5]["y"] < bounds[1]
        or history["actions"][-5]["y"] > bounds[3]
    ):
        return False

    # last two step
    parser = ETParser(history["xml"][-4])
    list_element = parser.get_element_bydic(
        {
            "resource-id": "com.contextlogic.wish:id/recycler",
            "class": "android.widget.GridView",
        }
    )

    if list_element is None:
        return False

    first_item = list_element.findall("*")[0]

    if first_item is None:
        return False

    if history["actions"][-4]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(first_item)
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

    # last step
    parser = ETParser(history["xml"][-3])
    wishlist_element = parser.get_element(
        "resource-id", "com.contextlogic.wish:id/wishlist"
    )

    if wishlist_element is None:
        return False

    if history["actions"][-3]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(wishlist_element)
    if clickable_parent is None:
        return False

    bounds = ETParser.get_bounds(clickable_parent)
    if (
        history["actions"][-3]["x"] < bounds[0]
        or history["actions"][-3]["x"] > bounds[2]
        or history["actions"][-3]["y"] < bounds[1]
        or history["actions"][-3]["y"] > bounds[3]
    ):
        return False

    # last step
    parser = ETParser(history["xml"][-2])
    select_wishlist_element = parser.get_element(
        "resource-id", "com.contextlogic.wish:id/fragment_select_wishlist_item_image"
    )

    if select_wishlist_element is None:
        return False

    if history["actions"][-2]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(select_wishlist_element)
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
