from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Go to recent updates in 'world news' section",
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
    element = parser.get_element("text", "World")

    if element is None:
        return False

    # find second world element
    world_bar_select_element = parser.get_element_contains_from(
        "text", "World", "text", "World"
    )

    if world_bar_select_element is None:
        return False

    parent_element = parser.find_parent(world_bar_select_element)

    if parent_element is None:
        return False

    if parent_element.attrib["selected"] == "false":
        return False

    return True
