from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open 'clips' section tab in Instagram.",
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
    element = parser.get_element("resource-id", "com.instagram.android:id/clips_tab")
    if element is not None:
        if element.attrib["selected"] == "true":
            return True
    return False
