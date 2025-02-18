# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    return {
        "task": "Provide details about the most recent video from my YouTube subscriptions.",
        "level": "easy",
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

    # Find the parent element with the specific resource-id
    parent_element = parser.get_element(
        "resource-id", "com.google.android.youtube:id/results"
    )
    if parent_element is None:
        # print(
        #     "Parent element with resource-id 'com.google.android.youtube:id/results' not found."
        # )
        return None

    # Iterate through its children to find the first element with 'content-desc'
    for child in parent_element.iter():
        content_desc = child.attrib.get("content-desc")
        if content_desc is not None:
            gt = content_desc
            judge = answer_correct_judge(
                task,
                answer,
                gt,
                client,
                model_type,
            )
            return judge
