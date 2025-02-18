import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "What are the details of 'Python Assignment1' in Google Tasks?",
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

    gt = ""

    task_element = parser.get_element_bydic(
        {
            "resource-id": "com.google.android.apps.tasks:id/task_name",
            "text": "Python Assignment1",
        }
    )

    if task_element is None:
        edit_element = parser.get_element_bydic(
            {
                "text": "Python Assignment1",
                "resource-id": "com.google.android.apps.tasks:id/edit_title",
            }
        )

        # check if agent is in edit mode
        if edit_element is None:
            return False

        edit_details_element = parser.get_element(
            "resource-id", "com.google.android.apps.tasks:id/edit_details"
        )

        if edit_details_element is None:
            return False

        gt = edit_details_element.attrib["text"]
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    task_details_element = parser.get_element_contains_from_until(
        "resource-id",
        "com.google.android.apps.tasks:id/task_details",
        "text",
        "Python Assignment1",
        "resource-id",
        "com.google.android.apps.tasks:id/tasks_item_completed_check",
    )

    if task_details_element is None:
        judge = answer_correct_judge(
            task,
            answer,
            'No details found for "Python Assignment1"',
            client,
            model_type,
        )
        return judge

    gt = task_details_element.attrib["text"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
