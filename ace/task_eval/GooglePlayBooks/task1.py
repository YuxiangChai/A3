from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open google play books' wishlist",
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
        "resource-id", "com.google.android.apps.books:id/bottom_wishlist"
    )
    if element is None:
        return False

    if element.attrib["selected"] != "true":
        return False

    wishlist_element = parser.get_element("content-desc", "Wishlist")

    if wishlist_element.attrib["selected"] != "true":
        return False

    return True
