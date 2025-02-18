from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open 'Notifications' panel in Booking.com app",
        "level": "easy",
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
    action_element = parser.get_element("resource-id", "com.booking:id/action_bar")

    if action_element is None:
        return False

    child_elements = action_element.findall("*")

    if len(child_elements) < 2:
        return False

    if child_elements[0].attrib["content-desc"].lower() != "navigate up":
        return False

    if child_elements[1].attrib["text"] != "Your Notifications":
        return False

    return True
