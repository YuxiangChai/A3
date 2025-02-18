# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Like the currently playing song in YouTube Music.",
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
    # Step 1: Verify that the action in history corresponds to the "like" tap within the expected region
    if len(history["actions"]) < 2:
        # print("Not enough actions in history.")
        return False

    like_action = history["actions"][-2]
    if not (35 <= like_action["x"] <= 291 and 1486 <= like_action["y"] <= 1581):
        # print("The last action was not within the 'Like' button region.")
        return False

    # Step 2: Retrieve the like count from xml[-2] (before like action)
    prev_parser = ETParser(history["xml"][-2])
    prev_like_count = None

    for el in prev_parser.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if "like this video along with" in content_desc.lower():
            prev_like_count_str = (
                content_desc.split("like this video along with")[1]
                .split(" ")[1]
                .replace(",", "")
            )
            prev_like_count = int(prev_like_count_str)
            break

    if prev_like_count is None:
        # print("Previous like count not found.")
        return False

    # Step 3: Retrieve the like count from xml[-1] (after like action)
    current_parser = ETParser(xml)
    current_like_count = None

    for el in current_parser.et.iter():
        content_desc = el.attrib.get("content-desc", "")
        if "like this video along with" in content_desc.lower():
            current_like_count_str = (
                content_desc.split("like this video along with")[1]
                .split(" ")[1]
                .replace(",", "")
            )
            current_like_count = int(current_like_count_str)
            break

    if current_like_count is None:
        # print("Current like count not found.")
        return False

    # Step 4: Compare the like counts to verify if it increased by 1
    if current_like_count == prev_like_count + 1:
        # print("Like action was successful.")
        return True
    else:
        # print("Like action was not successful.")
        return False
