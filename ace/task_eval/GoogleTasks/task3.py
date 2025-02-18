import glob
import xml.etree.ElementTree as ET

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In google tasks, sort my 'Homework' list by date. What is the most urgent task in 'Homework' list? When is it due?",
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
    parser = ETParser(history["xml"][-1])

    # check if it is Homework list
    list_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/task_list_title"
    )

    if list_element is None:
        return False

    if list_element.attrib["text"] != "Homework":
        return False

    # no task
    no_task_element = parser.get_element("text", "No tasks yet")

    if no_task_element is not None:
        gt = "No tasks in this list"
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    # all task completed
    all_task_complete_element = parser.get_element("text", "All tasks completed")

    if all_task_complete_element is not None:
        gt = "ALl tasks are completed in this list"
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge

    task_list_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/tasks_list"
    )

    # if it didn't sort
    if task_list_element.findall("*")[1].attrib["class"] != "android.widget.TextView":
        return False

    # sort wrongly
    if (
        task_list_element.findall("*")[1].attrib["text"] == "Starred recently"
        or task_list_element.findall("*")[1].attrib["text"] == "Not starred"
    ):
        return False

    task_element = parser.get_element(
        "resource-id", "com.google.android.apps.tasks:id/task_item_layout"
    )

    gt = task_element.attrib["content-desc"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
