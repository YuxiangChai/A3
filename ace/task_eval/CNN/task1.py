from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search news about 'panda' in CNN.",
        "level": "middle",
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
        "resource-id", "com.cnn.mobile.android.phone:id/toolbar_title"
    )
    if element is None:
        return False

    if element.attrib["text"].lower() != "search":
        return False

    result_element = parser.get_element_contains("text", "Results for")

    if result_element is None:
        return False

    if result_element.attrib["text"].find("panda") == -1:
        return False

    return True
