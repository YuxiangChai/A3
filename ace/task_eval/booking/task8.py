import re
from datetime import datetime, timedelta

from ace.utils.xml_parser import ETParser


def task() -> str:
    today = datetime.now()

    # 计算两天的日期
    day_1 = today + timedelta(days=2)
    day_2 = today + timedelta(days=4)

    # 打印后天的日期，格式为 "YYYY-MM-DD"
    formatted_date_1 = day_1.strftime("%Y-%m-%d")
    formatted_date_2 = day_2.strftime("%Y-%m-%d")

    return {
        "task": f"Open booking.com and search for car rentals. Set the Pick-up at University of Washington on {formatted_date_1}, drop-off at University of Washington on {formatted_date_2}, and also set filter to 'medium car with 5 seats at least'.",
        "level": "hard",
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
    parser = ETParser(xml)

    date_pattern = r"on\s(.*?),.*?on\s(.*?)$"
    dates = re.search(date_pattern, task)

    if dates:
        pickup_date = dates.group(1)
        dropoff_date = dates.group(2)

    # find option info
    element = parser.get_element_bydic(
        {
            "class": "android.widget.Button",
            "content-desc": f"Pick-up University of Washington {pickup_date}, drop-off University of Washington {dropoff_date}",
        }
    )
    if element is None:
        return False

    # find filter element
    filter_element = parser.get_element_bydic(
        {"text": "Filter", "class": "android.widget.TextView"}
    )
    if filter_element is None:
        return False

    # filter's parent element usually has 3 children elements when unselected, it has four when selected.
    filter_element_parent = parser.find_parent(filter_element)
    if len(filter_element_parent.findall("*")) < 4:
        return False

    if len(history["actions"]) < 3:
        return False

    parser = None
    tap_task = 2
    tap_completed = 0
    check_list = []
    for action_step in range(len(history["actions"]) - 2, -1, -1):
        # if tap_completed == tap_task:
        #     return True
        if history["actions"][action_step]["action"] == "tap":
            parser = ETParser(history["xml"][action_step])

            car_type_filter_element = parser.get_element_contains_from(
                "text", "Medium", "text", "Car Type"
            )

            if car_type_filter_element is not None:

                # Find clickable parent
                clickable_parent = parser.find_clickable_parent(car_type_filter_element)
                if clickable_parent is None:
                    return False

                bounds = ETParser.get_bounds(clickable_parent)
                if (
                    history["actions"][action_step]["action"] == "tap"
                    and history["actions"][action_step]["x"] > bounds[0]
                    and history["actions"][action_step]["x"] < bounds[2]
                    and history["actions"][action_step]["y"] > bounds[1]
                    and history["actions"][action_step]["y"] < bounds[3]
                ):
                    check_list.append(True)
                    continue

            seats_filter_element = parser.get_element_contains_from(
                "text", "5", "text", "Seats", 0
            )

            if seats_filter_element is not None:

                clickable_parent = parser.find_clickable_parent(seats_filter_element)
                if clickable_parent is None:
                    return False

                bounds = ETParser.get_bounds(clickable_parent)
                if (
                    history["actions"][action_step]["action"] == "tap"
                    and history["actions"][action_step]["x"] > bounds[0]
                    and history["actions"][action_step]["x"] < bounds[2]
                    and history["actions"][action_step]["y"] > bounds[1]
                    and history["actions"][action_step]["y"] < bounds[3]
                ):
                    check_list.append(True)
    if len(check_list) < 2:
        return False

    return check_list[0] and check_list[1]
