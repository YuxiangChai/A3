from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search for pizza near hong kong university on Yelp",
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

    if element is not None:
        if element.attrib["text"].lower() == "pizza hong kong university":
            return True
        if element.attrib["text"].lower() == "pizza hongkong university":
            return True
    return False
