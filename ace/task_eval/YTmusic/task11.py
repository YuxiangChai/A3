# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.screenshot_ocr import process_screenshot_with_bounds
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Let me know the most popular comment of the current playing song in YouTube Music.",
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
    def parse_bounds(bounds_str: str) -> tuple:
        """
        将 bounds 字符串解析为 (x1, y1, x2, y2) 元组。

        Args:
            bounds_str (str): 表示坐标范围的字符串，例如 "[127,710][427,752]"

        Returns:
            tuple: (x1, y1, x2, y2)
        """
        if not bounds_str:
            return None
        bounds_values = bounds_str.strip("[]").split("][")
        x1, y1 = map(int, bounds_values[0].split(","))
        x2, y2 = map(int, bounds_values[1].split(","))
        return (x1, y1, x2, y2)

    # Initialize XML parser
    parser = ETParser(xml)

    # Step 1: Find the parent element with the specific resource-id
    parent_element = parser.get_element(
        "resource-id", "com.google.android.apps.youtube.music:id/content"
    )
    if parent_element is None:
        # print(
        #     "Parent element with resource-id='com.google.android.apps.youtube.music:id/content' not found."
        # )
        return False

    # Step 2: Locate the first "android.widget.Button" element
    button_element = None
    for el in parent_element.iter():
        if el.attrib.get("class") == "android.widget.Button":
            button_element = el
            break

    if button_element is None:
        # print("Button element not found.")
        return False

    # Step 3: Traverse the parent to get bounds of relevant elements
    p_ele = parser.find_parent(button_element)
    bounds = []
    for el in p_ele.iter():
        bound_str = el.attrib.get("bounds", "")
        if bound_str:
            bounds.append(parse_bounds(bound_str))
        if len(bounds) >= 5:  # Limit to the first 5 bounds
            break

    if len(bounds) < 5:
        # print("Insufficient bounds data found.")
        return False

    # Extract specific bounds
    bound1 = bounds[3]  # Example: (127, 710, 427, 752)
    bound2 = bounds[4]  # Example: (85, 860, 1080, 986)

    # Construct new bounds based on the task's requirements
    if bound1 and bound2:
        newbound = (bound2[0], bound1[3], bound2[2], bound2[1])  # (x1, d, x2, y1)
    else:
        # print("Failed to construct new bounds.")
        return False

    # Step 4: Process screenshot to extract the GroundTruth
    gt = process_screenshot_with_bounds(screenshot, newbound)
    # print("Extracted GroundTruth:", GroundTruth)
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
