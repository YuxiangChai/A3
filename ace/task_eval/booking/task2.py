import re
from datetime import datetime, timedelta

from ace.utils.xml_parser import ETParser


def task() -> str:
    today = datetime.now()
    day_1 = today + timedelta(days=2)
    formatted_date_1 = day_1.strftime("%b %d")
    return {
        "task": f"In booking.com app, search one-way flight from Hong Kong to Beijing on {formatted_date_1} for 1 adault, economy class",
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
        "resource-id", "com.booking:id/flights_search_results_summary_search_options"
    )

    if option_element is None:
        return False

    # if any info is mis-matched, return false
    date_match = re.search(r"(?<=on\s).*?(?=\sfor)", task)
    date = date_match.group() if date_match else ""
    if (
        option_element.attrib["text"].lower().find(f"{date.lower()}") == -1
        or option_element.attrib["text"].lower().find("1 adult") == -1
        or option_element.attrib["text"].lower().find("economy") == -1
    ):
        return False

    return True
