import re
from datetime import datetime, timedelta

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
        "task": f"Search for 'car rentals' in Booking.com. And set Pick-up at University of Washington on {formatted_date_1}, Drop-off at University of Washington on {formatted_date_2}",
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
    return True
