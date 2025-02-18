import re
from datetime import datetime, timedelta

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    # 获取今天的日期
    today = datetime.now()

    # 计算两天的日期
    day_1 = today + timedelta(days=2)
    day_2 = today + timedelta(days=4)

    # 打印后天的日期，格式为 "YYYY-MM-DD"
    formatted_date_1 = day_1.strftime("%Y-%m-%d")
    formatted_date_2 = day_2.strftime("%Y-%m-%d")
    return {
        "task": f"Search car rentals in booking.com and set Pick-up at University of Washington on {formatted_date_1}, drop-off at University of Washington on {formatted_date_2}. Then sort results by price, and tell me the lowest price.",
        "level": "hard",
        "category": "single-page operation",
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
    if len(history["xml"]) < 2:
        return False

    parser = ETParser(xml)

    price_element = parser.get_element_contains("text", "US$")

    gt = price_element.attrib["text"]

    # find option info
    date_pattern = r"on\s(.*?),.*?on\s(.*?)$"
    dates = re.search(date_pattern, task)

    if dates:
        pickup_date = dates.group(1)
        dropoff_date = dates.group(2)
    element = parser.get_element_bydic(
        {
            "class": "android.widget.Button",
            "content-desc": f"Pick-up University of Washington {pickup_date}, drop-off University of Washington {dropoff_date}",
        }
    )

    if element is None:
        return False

    # find filter element
    sort_element = parser.get_element_bydic(
        {"text": "Sort", "class": "android.widget.TextView"}
    )
    if sort_element is None:
        return False

    # sort's parent element usually has 3 children elements when unselected, it has four when selected.
    sort_element_parent = parser.find_parent(sort_element)
    if len(sort_element_parent.findall("*")) < 4:
        return False

    # last step is to tap the sort by price
    parser = ETParser(history["xml"][-2])
    element = parser.get_element("text", "Price - lowest first")
    if element is None:
        return False

    # find its father element
    father_element = parser.find_parent(element)

    if father_element is None:
        return False

    bounds = ETParser.get_bounds(father_element)
    # if the last action is tap and it taps the right region
    if (
        history["actions"][-2]["action"] == "tap"
        and history["actions"][-2]["x"] > bounds[0]
        and history["actions"][-2]["x"] < bounds[2]
        and history["actions"][-2]["y"] > bounds[1]
        and history["actions"][-2]["y"] < bounds[3]
    ):
        judge = answer_correct_judge(
            task,
            answer,
            gt,
            client,
            model_type,
        )
        return judge
