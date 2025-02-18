from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Search linear algebra in coursera",
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
    search_element = parser.get_element("text", "Search")
    if search_element is None:
        return False

    search_la_element = parser.get_element("class", "android.widget.EditText")

    if search_la_element is None:
        return False

    if search_la_element.attrib["text"].lower() != "linear algebra":
        return False

    return True
