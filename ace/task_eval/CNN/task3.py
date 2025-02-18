from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "What is the current headline in the top news.",
        "level": "easy",
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
    topnews_element = parser.get_element("text", "Top News")

    if topnews_element is None:
        return False

    parent_element = parser.find_parent(topnews_element)

    if parent_element is None:
        return False

    if parent_element.attrib["selected"] != "true":
        return False

    first_top_news = parser.get_element_contains_from(
        "class", "android.widget.TextView", "clickable", "true"
    )

    gt = first_top_news.attrib["text"]

    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
