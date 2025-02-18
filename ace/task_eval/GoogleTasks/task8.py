import glob
import xml.etree.ElementTree as ET

from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Delete the 'Python Assignment1' task under 'Homework' list in Google Tasks.",
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
    stage = 1
    index = -1
    while index < len(history["xml"]) - 1:
        index += 1
        if stage == 1:
            parser = ETParser(history["xml"][index])
            homework_button = parser.get_element_bydic(
                {"package": "com.google.android.apps.tasks", "content-desc": "Homework"}
            )

            if homework_button is None:
                continue

            if homework_button.attrib["selected"] == "true":
                stage = 2
                continue
            else:

                # "[1,2][3,4]" -> [1,2,3,4]
                bounds_str = homework_button.attrib["bounds"].replace("][", ",")

                # 1. 去掉方括号
                bounds_str = bounds_str.strip("[]")

                # 2. 将字符串按逗号分割
                bounds = list(map(int, bounds_str.split(",")))

                action = history["actions"][index]
                # if click more action button
                if (
                    action["action"] == "tap"
                    and action["x"] > bounds[0]
                    and action["x"] < bounds[2]
                    and action["y"] > bounds[1]
                    and action["y"] < bounds[3]
                ):
                    stage = 2
                    continue

        # if stage is in homework list, agent should click 'Python Assignment1'
        elif stage == 2:
            parser = ETParser(history["xml"][index])
            homework_element = parser.get_element_bydic(
                {"package": "com.google.android.apps.tasks", "content-desc": "Homework"}
            )
            if homework_element is None:
                continue

            # if homework list is not selected, go back to previous stage
            if homework_element.attrib["selected"] != "true":
                stage = 1
                index -= 1
                continue

            task_button = parser.get_element_contains(
                "content-desc", "Python Assignment1"
            )

            if task_button is None:
                continue

            # "[1,2][3,4]" -> [1,2,3,4]
            bounds_str = task_button.attrib["bounds"].replace("][", ",")

            # 1. 去掉方括号
            bounds_str = bounds_str.strip("[]")

            # 2. 将字符串按逗号分割
            bounds = list(map(int, bounds_str.split(",")))

            action = history["actions"][index]
            # if click more action button
            if (
                action["action"] == "tap"
                and action["x"] > bounds[0]
                and action["x"] < bounds[2]
                and action["y"] > bounds[1]
                and action["y"] < bounds[3]
            ):
                stage = 3
                continue

        # if stage is in more option stage, at this stage, agent is suppose to click more options button
        elif stage == 3:
            parser = ETParser(history["xml"][index])
            more_option_button = parser.get_element("content-desc", "More options")

            if more_option_button is None:
                continue

            # "[1,2][3,4]" -> [1,2,3,4]
            bounds_str = more_option_button.attrib["bounds"].replace("][", ",")

            # 1. 去掉方括号
            bounds_str = bounds_str.strip("[]")

            # 2. 将字符串按逗号分割
            bounds = list(map(int, bounds_str.split(",")))

            action = history["actions"][index]
            # if click more action button
            if (
                action["action"] == "tap"
                and action["x"] > bounds[0]
                and action["x"] < bounds[2]
                and action["y"] > bounds[1]
                and action["y"] < bounds[3]
            ):
                stage = 4
                continue

            back_button = parser.get_element("content-desc", "Back")

            if back_button is None:
                continue

            # "[1,2][3,4]" -> [1,2,3,4]
            bounds_str = back_button.attrib["bounds"].replace("][", ",")

            # 1. 去掉方括号
            bounds_str = bounds_str.strip("[]")

            # 2. 将字符串按逗号分割
            bounds = list(map(int, bounds_str.split(",")))

            # if click back button
            if (
                action["action"] == "tap"
                and action["x"] > bounds[0]
                and action["x"] < bounds[2]
                and action["y"] > bounds[1]
                and action["y"] < bounds[3]
            ):
                stage = 2
                continue

        # if stage is in delete stage, at this stage, agent is suppose to click delete button.
        elif stage == 4:
            # click delete
            parser = ETParser(history["xml"][index])

            delete_button = parser.get_element_bydic(
                {
                    "text": "Delete",
                    "resource-id": "com.google.android.apps.tasks:id/title",
                }
            )

            if delete_button is None:
                return False

            # "[1,2][3,4]" -> [1,2,3,4]
            bounds_str = delete_button.attrib["bounds"].replace("][", ",")

            # 1. 去掉方括号
            bounds_str = bounds_str.strip("[]")

            # 2. 将字符串按逗号分割
            bounds = list(map(int, bounds_str.split(",")))

            # if it taps the right region
            action = history["actions"][index]
            if (
                action["action"] == "tap"
                and action["x"] > bounds[0]
                and action["x"] < bounds[2]
                and action["y"] > bounds[1]
                and action["y"] < bounds[3]
            ):
                return True
            else:
                stage = 3

    return False
