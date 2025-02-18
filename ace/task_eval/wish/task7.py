from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In wish app, go to 'best sellers'. Choose the first item and view comments, then tell me the overall rating",
        "level": "medium",
        "category": "single-page query",
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

    # click item rating
    parser = ETParser(history["xml"][-2])
    rating_element = parser.get_element(
        "resource-id", "com.contextlogic.wish:id/stars_rating_view"
    )

    if rating_element is None:
        return False

    if history["actions"][-2]["action"] != "tap":
        return False

    clickable_parent = parser.find_clickable_parent(rating_element)
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

    parser = ETParser(xml)
    overall_rating_element = parser.get_element(
        "resource-id", "com.contextlogic.wish:id/overall_rating"
    )
    gt = overall_rating_element.attrib["text"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
