# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open the comments section in Youtube music and sort comments by newest.",
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

    if len(history["actions"]) < 2:
        print("Insufficient action history for validation.")
        return False

    # Step 1: Check if the first tap action was within the comment button bounds
    comment_action = history["actions"][-3]
    if comment_action["action"] != "click":
        return False
    if not (445 <= comment_action["x"] <= 679 and 1486 <= comment_action["y"] <= 1581):
        # print("The comment section tap action was not within the expected bounds.")
        return False

    # Step 2: Check if the second tap action was within the "Newest" button bounds
    newest_action = history["actions"][-2]
    if not (180 <= newest_action["x"] <= 391 and 401 <= newest_action["y"] <= 527):
        # print("The 'Newest' sorting tap action was not within the expected bounds.")
        return False

    # print("Actions indicate that comments section is open and sorted by newest.")
    return True
