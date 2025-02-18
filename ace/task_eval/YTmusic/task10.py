# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open the history interface in YouTube Music.",
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

    # Step 2: Manually iterate over elements to check for text="History"
    for el in parser.et.iter():
        if el.attrib.get("text") == "History":
            # print("Element with text 'History' was found.")
            return True

    # print("Element with text 'History' was not detected.")
    return False
