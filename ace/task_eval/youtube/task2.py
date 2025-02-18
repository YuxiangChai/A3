# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "open the search fliters and choose sort by 'relevance' in youtube.",
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

    # 找到 "Sort by" 的父容器
    sort_by_element = parser.get_element(
        "resource-id", "com.google.android.youtube:id/label"
    )
    if (
        sort_by_element is not None
        and sort_by_element.attrib["text"].lower() == "sort by"
    ):
        parent_element = parser.find_parent(sort_by_element)

        if parent_element is not None:
            # 在父容器下寻找 resource-id 为 android:id/text1 的元素
            for child in parent_element.iter():
                if child.attrib.get("resource-id") == "android:id/text1":
                    # 检查是否 text 是 "relevance"
                    if child.attrib["text"].lower() == "relevance":
                        return True
    return False
