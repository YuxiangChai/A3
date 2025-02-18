# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Search the emails from 'autoreply002@hotmail.com' in Gmail.",
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
    email_xml = ETParser(xml)
    search_element = email_xml.get_element(
        "resource-id", "com.google.android.gm:id/open_search_bar_text_view"
    )
    if search_element is None:
        if search_element.attrib.get("text", "").strip() == "autoreply002@hotmail.com":
            return True
    return False
