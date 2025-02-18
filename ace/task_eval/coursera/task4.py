import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open Coursera and select free courses. What is the first course?",
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
    parser = ETParser(history["xml"][-1])
    topic_element = parser.get_element_bydic(
        {
            "text": "Get Started with These Free Courses",
            "class": "android.widget.TextView",
        }
    )

    if topic_element is None:
        return False

    list_element = parser.get_element("class", "android.widget.ScrollView")

    if list_element is None:
        return False

    first_course_element = list_element.findall("*")[0]

    if first_course_element is None:
        return False

    first_course_detail_element = first_course_element.findall("*")[0]

    gt = first_course_detail_element.attrib["content-desc"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
