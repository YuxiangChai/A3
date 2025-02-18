import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from ace.utils.avd_control import Controller
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "In google tasks, which task is the most urgent one in 'Math homework', 'English homework' and 'History homework' lists?",
        "level": "hard",
        "category": "multi-page query",
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
    index = -1
    dates = [0] * 3
    tasks = [0] * 3
    dues = [0] * 3
    lists = ["Math homework", "English homework", "History homework"]
    while index < len(history["xml"]) - 1:
        index += 1

        parser = ETParser(history["xml"][index])

        # check if the list is right
        list_title_element = parser.get_element(
            "resource-id", "com.google.android.apps.tasks:id/task_list_title"
        )

        if list_title_element is None:
            continue

        list_name = list_title_element.attrib["text"]
        if list_name not in lists:
            continue

        empty_check_element = parser.get_element(
            "resource-id", "com.google.android.apps.tasks:id/tasks_empty_state_header"
        )

        if empty_check_element is not None:
            i = lists.index(list_name)
            dates[i] = None
            tasks[i] = None
            continue

        list_element = parser.get_element(
            "resource-id", "com.google.android.apps.tasks:id/tasks_list"
        )

        if list_element is None:
            continue

        element = list_element.findall("*")[1]
        empty_flag = False
        date = None
        date_title = None

        for element in list_element.findall("*"):
            if element.attrib["class"] != "android.widget.TextView":
                continue
            # ignore the past task
            if element.attrib["text"] == "Past":
                empty_flag = True
                continue
            elif element.attrib["text"] == "Today":
                date_title = element
                empty_flag = False
                date = datetime.today()

                break
            elif element.attrib["text"] == "Tomorrow":
                date_title = element
                empty_flag = False
                date = datetime.today() + timedelta(days=1)

                break
            else:
                # check if the list are sort by date
                try:
                    # 尝试解析日期字符串
                    date = datetime.strptime(element.attrib["text"], "%a, %b %d")
                    empty_flag = False
                    date_title = element

                    break
                except ValueError:
                    break

        if empty_flag:
            i = lists.index(list_name)
            dates[i] = None
            tasks[i] = None
            continue

        if date is None:
            continue

        task_element = parser.get_element_contains_from_element(
            "resource-id", "com.google.android.apps.tasks:id/task_name", date_title
        )

        if task_element is None:
            continue

        due_time_element = parser.get_element_contains_from_element(
            "resource-id",
            "com.google.android.apps.tasks:id/task_due_date_text",
            date_title,
        )

        if due_time_element is None:
            due = ""
        else:
            due = due_time_element.attrib["text"]
        if list_name == "Math homework":
            dates[0] = date
            tasks[0] = task_element.attrib["text"]
            dues[0] = due
        elif list_name == "English homework":
            dates[1] = date
            tasks[1] = task_element.attrib["text"]
            dues[1] = due
        elif list_name == "History homework":
            dates[2] = date
            tasks[2] = task_element.attrib["text"]
            dues[2] = due

    most_urgent_date = datetime(2999, 12, 31)
    most_urgent_task = ""
    ddl = ""
    for date, task, due in zip(dates, tasks, dues):
        # not assigned
        if date == 0:
            return False
        # list is empty
        if date is None:
            continue
        if date < most_urgent_date:
            most_urgent_date = date
            most_urgent_task = task
            ddl = due
    gt = f"The most urgent task is:{most_urgent_task}, it dues at:{most_urgent_date.strftime('%b, %d')} {ddl}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
