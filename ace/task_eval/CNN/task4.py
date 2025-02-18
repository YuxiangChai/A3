from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "What is the current headline in U.S. politics.",
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
    usp_element = parser.get_element("text", "U.S. Politics")

    if usp_element is None:
        return False

    parent_element = parser.find_parent(usp_element)

    if parent_element is None:
        return False

    if parent_element.attrib["selected"] != "true":
        return False

    first_clickable_news = parser.get_element("clickable", "true")

    first_usp_news = first_clickable_news.findall("*")[1]

    gt = first_usp_news.attrib["text"]

    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
