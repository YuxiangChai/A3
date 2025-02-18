from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open 'shelves' in Google Play Books.",
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
    parser = ETParser(history["xml"][-1])
    library_element = parser.get_element(
        "resource-id", "com.google.android.apps.books:id/bottom_library"
    )

    if library_element is None:
        return False

    if library_element.attrib["selected"] != "true":
        return False

    shelves_element = parser.get_element("content-desc", "Shelves")

    if shelves_element is None:
        return False

    if shelves_element.attrib["selected"] != "true":
        return False

    return True
