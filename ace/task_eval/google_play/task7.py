# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "What is the top-ranked app in Google Play's paid Top Charts.",
        "level": "medium",
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
    parser = ETParser(xml)

    # Find the element with text="1"
    rank_one_element = None
    for element in parser.et.iter():
        if element.attrib.get("text") == "1":
            rank_one_element = element
            break

    if rank_one_element is None:
        # print('Element with text="1" not found.')
        return None

    # Find the next sibling of the rank-one element
    top_app_element = None
    parent = None

    for el in parser.et.iter():
        if rank_one_element in el:
            parent = el
            break

    if parent is None:
        # print("Parent element of the rank-one element not found.")
        return None

    found_rank_one = False
    for child in parent:
        if child == rank_one_element:
            found_rank_one = True
            continue
        if found_rank_one:
            content_desc = child.attrib.get("content-desc")
            if content_desc:
                top_app_element = child
                break

    if top_app_element is None:
        # print("Top app's element not found.")
        return None

    # Extract the app name from the content-desc attribute
    content_desc = top_app_element.attrib.get("content-desc", "")
    app_name = content_desc.split("&#10;")[
        0
    ]  # Extract the first part before the first &#10;

    gt = f"The top-ranked app is: {app_name}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
