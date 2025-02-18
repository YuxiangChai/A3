import re
from datetime import datetime, timedelta

from ace.utils.xml_parser import ETParser


def task() -> str:
    # 获取今天的日期
    today = datetime.now()

    # 计算后天的日期
    day_1 = today + timedelta(days=2)
    day_2 = today + timedelta(days=3)

    # 打印后天的日期，格式为 "Nov 27"
    formatted_date_1 = day_1.strftime("%b %d")
    formatted_date_2 = day_2.strftime("%b %d")
    return {
        "task": f"Search for hotel stays in Beijing from {formatted_date_1} to {formatted_date_2} in Booking.com app",
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

    # find option info
    des_element = parser.get_element(
        "resource-id", "com.booking:id/searchbox_destination"
    )

    if des_element is None:
        return False

    # if destination info is mis-matched, return false
    if des_element.attrib["text"].lower().find("beijing") == -1:
        return False

    dates_element = parser.get_element("resource-id", "com.booking:id/searchbox_dates")

    if dates_element is None:
        return False

    # if dates info is mis-matched, return false
    date_pattern = r"from\s(.*?)\sto\s(.*?)\sin"
    dates = re.search(date_pattern, task)

    if dates:
        date1, date2 = dates.group(1), dates.group(2)

    if (
        dates_element.attrib["text"].lower().find(f"{date1.lower()} - {date2.lower()}")
        == -1
    ):
        return False

    return True
