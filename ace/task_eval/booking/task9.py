import re
from datetime import datetime, timedelta

from ace.utils.xml_parser import ETParser


def task() -> str:
    # 获取今天的日期
    today = datetime.now()

    # 计算后天的日期
    day_1 = today + timedelta(days=2)

    # 打印后天的日期，格式为 "Nov 27"
    formatted_date_1 = day_1.strftime("%b %d")

    # 获取星期几
    day_of_week = day_1.strftime("%a")
    return {
        "task": f"In booking.com, reserve a taxi from CUHK to HKU, on {formatted_date_1}, 01:26PM",
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
    choice_element = parser.get_element_bydic(
        {
            "resource-id": "com.booking:id/search_results_title",
            "text": "Choose your ride",
        }
    )
    if choice_element is None:
        return False

    date_pattern = r"on\s(.*?),\s\d{2}:\d{2}(?:AM|PM)"
    date_match = re.search(date_pattern, task)

    if date_match:
        date = date_match.group(1)
        day_of_week = datetime.strptime(date, "%b %d").strftime("%a")

    search_bar_info_element = parser.get_element_contains_from(
        "content-desc",
        f"One-way trip for 2 passengers from The Chinese University of Hong Kong to University of Hong Kong (HKU). Pick-up is on {day_of_week} {date} at 01:26 PM.",
        "resource-id",
        "com.booking:id/search_header",
    )

    if search_bar_info_element is None:
        return False

    return True
