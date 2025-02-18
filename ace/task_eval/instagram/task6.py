from ace.utils.avd_control import Controller
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In Instagram, go to 'my following' section and then select 'Taylor Swift' and like her latest post. How many likes are there for the post?",
        "level": "hard",
        "category": "single-page query",
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

    liked_element = parser.get_element_contains_from(
        "class",
        "android.widget.Button",
        "resource-id",
        "com.instagram.android:id/row_feed_button_like",
    )

    if liked_element is None:
        return False

    gt = liked_element.attrib["text"]

    element = parser.get_element(
        "resource-id", "com.instagram.android:id/row_feed_button_like"
    )
    if element is not None:
        if element.attrib["selected"] == "true":
            judge = answer_correct_judge(
                task,
                answer,
                gt,
                client,
                model_type,
            )
            return judge
    return False
