from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search for burger at current location in Yelp, and filter results by 'good for kids'",
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
    element = parser.get_element(
        "resource-id", "com.yelp.android:id/pablo_toolbar_search_text"
    )

    if element is None:
        return False

    if element.attrib["text"].lower() != "burger current location":
        return False

    gfk_element = parser.get_element("text", "Good for Kids ")

    if gfk_element is None:
        return False

    return True
