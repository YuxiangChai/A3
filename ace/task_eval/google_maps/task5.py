# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    return {
        "task": "Sort search results by distance in Google Maps after searching for 'BBQ'.",
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
    relevance_xml = ETParser(history["xml"][-3])
    relevance_element = relevance_xml.get_element("text", "Relevance")
    if relevance_element is None:
        return False

    r_x1, r_y1, r_x2, r_y2 = relevance_xml.get_bounds(relevance_element)
    relevance_action = history["actions"][-3]
    if not (
        r_x1 <= relevance_action["x"] <= r_x2 and r_y1 <= relevance_action["y"] <= r_y2
    ):
        return False

    distance_xml = ETParser(history["xml"][-2])
    distance_element = distance_xml.get_element("text", "Distance")
    if distance_element is None:
        return False

    d_x1, d_y1, d_x2, d_y2 = distance_xml.get_bounds(distance_element)
    distance_action = history["actions"][-2]
    if not (
        d_x1 <= distance_action["x"] <= d_x2 and d_y1 <= distance_action["y"] <= d_y2
    ):
        return False

    result_xml = ETParser(history["xml"][-1])
    distance_text_element = result_xml.get_element("text", "Distance")
    return distance_text_element is not None
