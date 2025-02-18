from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "IN Yelp, search for 'burger' at current location. Then sort results by distance and filter by 'open at 11:00 pm'",
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
    parser = ETParser(xml)
    element = parser.get_element(
        "resource-id", "com.yelp.android:id/pablo_toolbar_search_text"
    )

    if element is None:
        return False

    if element.attrib["text"].lower() != "burger current location":
        return False

    sort_element = parser.get_element("text", "Sort: Distance")

    if sort_element is None:
        return False

    open_element = parser.get_element("text", "Open at 11:00 pm")

    if open_element is None:
        return False

    return True
