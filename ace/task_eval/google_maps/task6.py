# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    return {
        "task": "Search for BBQ in Google Maps, select the first store, and start navigation.",
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
    search_xml = ETParser(history["xml"][-3])
    search_box_element = search_xml.get_element("content-desc", "bbq")
    if search_box_element is None:
        return False

    directions_element = search_xml.get_element("text", "Directions")
    if directions_element is None:
        return False

    dx1, dy1, dx2, dy2 = search_xml.get_bounds(directions_element)
    directions_action = history["actions"][-3]
    if not (
        dx1 <= directions_action["x"] <= dx2 and dy1 <= directions_action["y"] <= dy2
    ):
        return False

    start_xml = ETParser(history["xml"][-2])
    start_element = start_xml.get_element("text", "Start")
    if start_element is None:
        return False

    sx1, sy1, sx2, sy2 = start_xml.get_bounds(start_element)
    start_action = history["actions"][-2]
    return sx1 <= start_action["x"] <= sx2 and sy1 <= start_action["y"] <= sy2
