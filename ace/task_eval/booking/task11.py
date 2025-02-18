import re
from datetime import datetime, timedelta

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    # 获取今天的日期
    today = datetime.now()

    # 计算后天的日期
    day_1 = today + timedelta(days=2)

    # 打印后天的日期，格式为 "Nov 27"
    formatted_date_1 = day_1.strftime("%b %d")
    return {
        "task": f"Open booking.com and search for one-way flights for 1 adault, economy class from Hong Kong to London on {formatted_date_1}. Which flight is the cheapest? How much is it?",
        "level": "hard",
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

    parser = ETParser(xml)

    # sort info
    sort_element = parser.get_element("text", "Sort by: Cheapest")
    if sort_element is None:
        return False

    # find route info
    route_element = parser.get_element(
        "resource-id", "com.booking:id/flights_search_results_summary_routes"
    )
    if route_element is None:
        return False

    route_children = route_element.findall("*")
    # at least two children
    if len(route_children) >= 2:
        # if its departure is not hong kong
        if route_children[0].attrib["text"].lower().find("hong kong") == -1:
            return False
        # if its destination is not london
        if route_children[1].attrib["text"].lower().find("london") == -1:
            return False

    # find option info
    option_element = parser.get_element(
        "resource-id", "com.booking:id/flights_search_results_summary_search_options"
    )

    if option_element is None:
        return False

    # if any info is mis-matched, return false
    date_pattern = r"on\s(.*?)(?=\.)"
    date_match = re.search(date_pattern, task)

    if date_match:
        date = date_match.group(1)
    if (
        option_element.attrib["text"].lower().find(f"{date.lower()}") == -1
        or option_element.attrib["text"].lower().find("1 adult") == -1
        or option_element.attrib["text"].lower().find("economy") == -1
    ):
        return False

    price_element = parser.get_element_contains("text", "HK$")

    gt = price_element.attrib["text"]
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
