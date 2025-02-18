from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In Instagram, post a photo in the album with any text.",
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
    parser = ETParser(xml)
    element = parser.get_element(
        "resource-id", "com.instagram.android:id/row_pending_media_status_textview"
    )
    if element is not None:
        if element.attrib["text"].lower().find("Done posting") != -1:
            return True
    return False
