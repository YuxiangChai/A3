from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open booking.com app and navigate to 'Saved' tab.",
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
        "resource-id", "com.booking:id/navigation_bar_item_large_label_view"
    )
    if element is not None:
        if element.attrib["text"].lower() == "saved":
            return True
    return False
