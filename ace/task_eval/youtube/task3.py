# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Open the youtube notifications settings and switch on the 'recommended videos'.",
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

    # 查找所有符合条件的元素
    title_elements = parser.get_elements(".//*[@resource-id='android:id/title']")

    for title_element in title_elements:
        if title_element.attrib["text"].lower() == "recommended videos":
            # 找到父容器 (RelativeLayout)
            parent_element = parser.find_parent(title_element)
            if parent_element is not None:
                # 找到祖父容器 (LinearLayout)
                grandparent_element = parser.find_parent(parent_element)
                if grandparent_element is not None:
                    # 在祖父容器内寻找 Switch 元素
                    switch_element = grandparent_element.find(
                        ".//*[@resource-id='android:id/switch_widget']"
                    )
                    if switch_element is not None:
                        # 检查 enabled 状态
                        return switch_element.attrib["checked"].lower() == "true"

    return False
