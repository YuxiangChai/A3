from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open 'clips' tab in Instagram. Then like the first two clips.",
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
    steps = len(history["xml"])
    # like two videos take at least 3 steps.
    if steps < 3:
        return False

    number_of_video_liked = 2

    for i in range(number_of_video_liked):
        parser = ETParser(history["xml"][steps - 1 - (i * 2)])
        element = parser.get_element(
            "resource-id", "com.instagram.android:id/like_button"
        )
        if element is not None:
            if element.attrib["selected"] == "false":
                return False
        else:
            return False
    return True
