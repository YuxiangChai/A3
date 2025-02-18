from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search 'Taylor Swift' on Instagram, and then follow the first account it shows",
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
        "resource-id", "com.instagram.android:id/profile_header_follow_button"
    )
    if element is not None:
        if element.attrib["text"].lower() == "following":
            return True
    return False
