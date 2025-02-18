from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open the current headline in U.S. politics in CNN.",
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
    parser = ETParser(history["xml"][-2])
    usp_element = parser.get_element("text", "U.S. Politics")

    if usp_element is None:
        return False

    parent_element = parser.find_parent(usp_element)

    if parent_element is None:
        return False

    if parent_element.attrib["selected"] != "true":
        return False

    first_clickable_news = parser.get_element("clickable", "true")

    first_usp_news = first_clickable_news.findall("*")[1]

    gt = first_usp_news.attrib["text"]

    parser = ETParser(xml)

    title_element = parser.get_element_contains_from(
        "text", gt, "class", "androidx.compose.ui.platform.ComposeView"
    )

    if title_element is None:
        return False

    return True
