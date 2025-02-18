# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Pause the currently playing song in the YouTube Music app.",
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
    """
    Evaluates whether the task of pausing the currently playing song in YouTube Music has been completed.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if the song was paused successfully, False otherwise.
    """
    # Step 1: Confirm the previous action was a "pause" tap within the expected region
    # if len(history["actions"]) < 2:
    #     # print("Not enough actions in history.")
    #     return False

    # pause_action = history["actions"][-2]
    # if not (445 <= pause_action["x"] <= 634 and 1747 <= pause_action["y"] <= 1936):
    #     # print("The second last action was not within the 'Pause' button region.")
    #     return False

    # # Step 2: Verify the state in xml[-2] (before pause) - Check if "Pause video" button was visible
    # prev_parser = ETParser(history["xml"][-2])
    # found_play_button = any(
    #     el.attrib.get("resource-id")
    #     == "com.google.android.apps.youtube.music:id/player_control_play_pause_replay_button"
    #     and el.attrib.get("content-desc") == "Pause video"
    #     for el in prev_parser.et.iter()
    # )

    # if not found_play_button:
    #     # print("Play button was not found in the previous state. Expected 'Pause video'.")
    #     return False

    # Step 3: Verify the state in the current xml (after pause) - Check if "Play video" button is now visible
    current_parser = ETParser(xml)
    found_pause_button = any(
        el.attrib.get("resource-id")
        == "com.google.android.apps.youtube.music:id/player_control_play_pause_replay_button"
        and el.attrib.get("content-desc") == "Play video"
        for el in current_parser.et.iter()
    )

    if found_pause_button:
        # print("Pause button confirmed, the song is paused.")
        return True
    else:
        # print("Pause button not found in the final state.")
        return False
