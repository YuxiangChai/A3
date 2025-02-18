# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Switch the Google Calendar viewing method to weekly viewing.",
        "level": "medium",
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

    # Step 3: 查找目标元素
    container_element = parser.get_element(
        "resource-id",
        "com.google.android.calendar:id/alternate_timeline_fragment_container",
    )
    if container_element is None:
        # print("Error: Target container element not found.")
        return False

    # Step 4: 遍历目标元素的子元素的子元素
    count = 0  # 统计 content-desc 不为空的元素数量
    for child in container_element:
        for sub_child in child:
            content_desc = sub_child.attrib.get("content-desc", "").strip()
            if content_desc:  # 判断 content-desc 不为空
                count += 1

    # Step 5: 检测数量是否恰好为 7
    if count == 7:
        # print("Success: Found exactly 7 elements with non-empty 'content-desc'.")
        return True
    else:
        # print(
        #     f"Failure: Found {count} elements with non-empty 'content-desc', expected 7."
        # )
        return False
