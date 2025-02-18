# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    return {
        "task": "Switch Google Maps layer to Satellite view.",
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
    layers_xml = ETParser(history["xml"][-4])
    layers_element = layers_xml.get_element(
        "resource-id", "com.google.android.apps.maps:id/layers_fab"
    )
    if layers_element is None:
        return False

    lx1, ly1, lx2, ly2 = layers_xml.get_bounds(layers_element)
    layers_action = history["actions"][-4]
    if not (lx1 <= layers_action["x"] <= lx2 and ly1 <= layers_action["y"] <= ly2):
        return False

    satellite_xml = ETParser(history["xml"][-3])
    satellite_element = satellite_xml.get_element("content-desc", "Satellite")
    if satellite_element is None:
        return False

    sx1, sy1, sx2, sy2 = satellite_xml.get_bounds(satellite_element)
    satellite_action = history["actions"][-3]
    if not (
        sx1 <= satellite_action["x"] <= sx2 and sy1 <= satellite_action["y"] <= sy2
    ):
        return False

    final_xml = ETParser(history["xml"][-2])
    satellite_status_element = final_xml.get_element("content-desc", "Satellite")
    return (
        satellite_status_element is not None
        and satellite_status_element.attrib.get("checked") == "true"
    )
