# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Comment on 'Excellent music' in the comments section.",
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
    # Step 1: Parse the latest XML in history
    parser = ETParser(history["xml"][-2])

    # Step 2: Iterate through elements to find one with normalized text and content-desc
    target_text = "Excellent music".strip().lower()
    for el in parser.et.iter():
        text = el.attrib.get("text", "").strip().lower()
        content_desc = el.attrib.get("content-desc", "").strip().lower()

        if text == target_text and content_desc == target_text:
            # print("Text input action was successful.")
            return True

    # print("Text input action was not detected.")
    return False
