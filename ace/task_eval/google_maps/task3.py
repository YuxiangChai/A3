# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    return {
        "task": "in google maps, swipe horizontally through suggestions under the search box to find and select 'Gas'.",
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
    swipe_action = history["actions"][-2]
    if swipe_action.get("action") != "swipe":
        return False

    suggestion_xml = ETParser(history["xml"][-1])
    gas_element = suggestion_xml.get_element("content-desc", "Gas")
    return gas_element is not None
