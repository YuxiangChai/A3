# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Open Youtube music and play the second song in Taylor Swift's top songs list.",
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
    """
    Evaluates whether the task of playing the second song in Taylor Swift's top songs list has been completed.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (list[dict]): Historical context, including XML and actions.

    Returns:
        bool: True if the second song is currently playing, False otherwise.
    """
    # Step 1: Retrieve the name of the second song in the top songs list from xml[-2]
    prev_parser = ETParser(history["xml"][-2])
    song_elements = [
        el
        for el in prev_parser.et.iter()
        if el.attrib.get("resource-id")
        == "com.google.android.apps.youtube.music:id/title"
    ]

    if len(song_elements) < 2:
        # print("Unable to locate the second song in the top songs list.")
        return False

    second_song_name = song_elements[1].attrib.get("text", "").strip()
    if not second_song_name:
        # print("The second song's name is missing.")
        return False

    # Step 2: Check if the current song being played matches this name in xml[-1]
    current_parser = ETParser(history["xml"][-1])
    playing_song_match = any(
        el.attrib.get("text", "").strip() == second_song_name
        for el in current_parser.et.iter()
        if el.attrib.get("resource-id")
        == "com.google.android.apps.youtube.music:id/current_song_view"
    )

    if playing_song_match:
        # print(f"The song '{second_song_name}' is currently playing as expected.")
        return True
    else:
        # print(f"The song '{second_song_name}' is not playing. Evaluation failed.")
        return False
