from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Navigate to 'recently viewed' in Wish app",
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
    element = parser.get_element_contains_from(
        "text",
        "Recently viewed",
        "resource-id",
        "com.contextlogic.wish:id/drawer_activity_toolbar",
    )

    if element is None:
        element = parser.get_element_contains_from(
            "text",
            "Recently Viewed",
            "resource-id",
            "com.contextlogic.wish:id/drawer_activity_toolbar",
        )

    if element is None:
        return False

    return True
