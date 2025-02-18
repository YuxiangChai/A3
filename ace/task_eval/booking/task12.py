import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": f"In Booking.com, search for one night stay for one-bed room at Hilton Gardon Inn Hong Kong in the next week. Which day is the cheapest? How much is it?",
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
    if len(history["xml"]) < 7:
        return False

    today = datetime.now()
    days_ahead = 7 - today.weekday()
    next_monday = today + timedelta(days=days_ahead)
    next_2 = next_monday + timedelta(1)
    next_3 = next_monday + timedelta(2)
    next_4 = next_monday + timedelta(3)
    next_5 = next_monday + timedelta(4)
    next_6 = next_monday + timedelta(5)
    next_7 = next_monday + timedelta(6)
    next_8 = next_monday + timedelta(7)

    # Date format : Dec 1
    dates = [
        next_monday.strftime("%b %#d"),
        next_2.strftime("%b %#d"),
        next_3.strftime("%b %#d"),
        next_4.strftime("%b %#d"),
        next_5.strftime("%b %#d"),
        next_6.strftime("%b %#d"),
        next_7.strftime("%b %#d"),
        next_8.strftime("%b %#d"),
    ]

    price_list = [0] * 7
    i = 0
    for xml in history["xml"]:
        i += 1
        parser = ETParser(xml)

        properties_element = parser.get_element_contains_from_until(
            "text",
            "properties",
            "resource-id",
            "com.booking:id/sr_saba_client_container",
        )

        if properties_element is None:
            continue

        search_element = parser.get_element(
            "resource-id", "com.booking:id/searchbox_destination"
        )

        if search_element is None:
            return False

        if (
            search_element.attrib["text"].lower()
            != "hilton garden inn hong kong mongkok"
        ):
            return False

        # find date info
        date_element = parser.get_element(
            "resource-id", "com.booking:id/searchbox_dates"
        )

        if date_element is None:
            return False

        # find price element
        price_element = parser.get_element_contains("text", "US$")
        price = price_element.attrib["text"]
        d = f"{dates[0].lower()} - {dates[1].lower()}"

        if (
            date_element.attrib["text"].lower()
            == f"{dates[0].lower()} - {dates[1].lower()}"
        ):
            price_list[0] = price
        elif (
            date_element.attrib["text"].lower()
            == f"{dates[1].lower()} - {dates[2].lower()}"
        ):
            price_list[1] = price
        elif (
            date_element.attrib["text"].lower()
            == f"{dates[2].lower()} - {dates[3].lower()}"
        ):
            price_list[2] = price
        elif (
            date_element.attrib["text"].lower()
            == f"{dates[3].lower()} - {dates[4].lower()}"
        ):
            price_list[3] = price
        elif (
            date_element.attrib["text"].lower()
            == f"{dates[4].lower()} - {dates[5].lower()}"
        ):
            price_list[4] = price
        elif (
            date_element.attrib["text"].lower()
            == f"{dates[5].lower()} - {dates[6].lower()}"
        ):
            price_list[5] = price
        elif (
            date_element.attrib["text"].lower()
            == f"{dates[6].lower()} - {dates[7].lower()}"
        ):
            price_list[6] = price
        else:
            return False

    lowest_price = 999999
    lowest_index = 0
    same_price_list = []

    for i in range(len(price_list)):
        # if any of the price havent't updated, it means it didn't get all information
        if price_list[i] == 0:
            return False
        new_price = int(
            price_list[i]
            .replace("US$", "")
            .replace("\u200e", "")
            .replace("\u202c", "")
            .strip()
        )
        if lowest_price == new_price:
            same_price_list.append(i)
        if lowest_price > new_price:
            lowest_price = new_price
            lowest_index = i
            same_price_list.clear()

    # 获取与最低价格相同的所有日期
    same_price_dates = [dates[i] for i in same_price_list]

    same_price_dates.insert(0, dates[lowest_index])

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
