from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In yelp, find home cleanning around current location. What is the overall rating of first result?",
        "level": "medium",
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
    element = parser.get_element(
        "resource-id", "com.yelp.android:id/pablo_toolbar_search_text"
    )

    if element is None:
        return False

    if element.attrib["text"].lower() != "home cleaning current location":
        return False

    review_element = parser.get_element(
        "resource-id", "com.yelp.android:id/review_count"
    )

    gt = review_element.attrib["text"]

    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
