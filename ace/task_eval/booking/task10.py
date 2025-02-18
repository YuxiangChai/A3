import glob
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    # 获取今天的日期
    today = datetime.now()

    # 计算后三天的日期
    day_1 = today + timedelta(days=1)

    # 打印后天的日期，格式为 "Nov 27"
    formatted_date_1 = day_1.strftime("%b %d")

    return {
        "task": f"In booking.com, search for one-way flights for 1 adault, economy class from Hong Kong to Beijing for the next 3 days starting from {formatted_date_1}. What is the lowest price and on which date?",
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
    if len(history["xml"]) < 3:
        return False

    date_pattern = r"starting from\s(.*?)(?=\.)"
    date_match = re.search(date_pattern, task)

    if date_match:
        date1 = date_match.group(1)
        date2 = datetime.strptime(date1, "%b %d") + timedelta(days=1)
        date3 = datetime.strptime(date1, "%b %d") + timedelta(days=2)

    formatted_dates = [
        date1,
        date2.strftime("%b %d"),
        date3.strftime("%b %d"),
    ]

    price_list = [0, 0, 0]
    i = 0
    for xml in history["xml"]:
        i += 1
        parser = ETParser(xml)

        results_element = parser.get_element_contains_from_until(
            "text",
            "results",
            "resource-id",
            "com.booking:id/facet_with_bui_booking_header_toolbar",
            "resource-id",
            "com.booking:id/facet_with_bui_booking_header_content",
        )

        if results_element is None:
            continue

        # sort info
        sort_element = parser.get_element("text", "Sort by: Cheapest")
        if sort_element is None:
            continue

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
            # if its destination is not beijing
            if route_children[1].attrib["text"].lower().find("beijing") == -1:
                return False

        # find option info
        option_element = parser.get_element(
            "resource-id",
            "com.booking:id/flights_search_results_summary_search_options",
        )

        if option_element is None:
            return False

        # # if passenger and class info is mis-matched, return false
        if (
            option_element.attrib["text"].lower().find("1 adult") == -1
            or option_element.attrib["text"].lower().find("economy") == -1
        ):
            return False

        # find price element
        price_element = parser.get_element_contains("text", "HK$")
        price = price_element.attrib["text"]
        option_str = option_element.attrib["text"].lower()

        # if it get info at certain date, update corresponding price
        if option_str.find(f"{date1.lower()}") != -1:
            price_list[0] = price

        elif option_str.find(f"{formatted_dates[1].lower()}") != -1:
            price_list[1] = price

        elif option_str.find(f"{formatted_dates[2].lower()}") != -1:
            price_list[2] = price

    lowest_price = 999999
    lowest_index = 0
    same_price_list = []

    for i in range(len(price_list)):
        # if any of the price havent't updated, it means it didn't get all information
        if price_list[i] == 0:
            return False
        new_price = int(price_list[i].replace("HK$", "").replace("\xa0", "").strip())
        if lowest_price == new_price:
            same_price_list.append(i)
        if lowest_price > new_price:
            lowest_price = new_price
            lowest_index = i
            same_price_list.clear()

    # 获取与最低价格相同的所有日期
    same_price_dates = [formatted_dates[i] for i in same_price_list]

    same_price_dates.insert(0, formatted_dates[lowest_index])

    # 将所有日期连接成一个字符串
    dates_string = ", ".join(same_price_dates)

    gt = f"{price_list[lowest_index]} at {dates_string}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
