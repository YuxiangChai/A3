# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Check my subscriptions and arrange them by 'most relevant' in YouTube.",
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
    element = parser.get_element("resource-id", "com.google.android.youtube:id/title")
    if element is not None:
        if element.attrib["text"].lower() == "most relevant":
            return True
    return False
