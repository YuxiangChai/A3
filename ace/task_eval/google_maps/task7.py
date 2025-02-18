# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    return {
        "task": "Tell me where is and how far is the nearest McDonald's on Google Maps.",
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

    top_parent = None
    for element in parser.et.iter():
        if (
            element.attrib.get("resource-id")
            == "com.google.android.apps.maps:id/search_list_layout"
        ):
            top_parent = element
            break

    if top_parent is None:
        return None

    texts = []
    found_first_relative_layout = False

    for child in top_parent.iter():
        if (
            child.attrib.get("class") == "android.widget.RelativeLayout"
            and not found_first_relative_layout
        ):
            found_first_relative_layout = True

        if found_first_relative_layout:
            text = child.attrib.get("text", "").strip()
            if text:
                texts.append(text)

        if (
            child.attrib.get("resource-id")
            == "com.google.android.apps.maps:id/recycler_view"
            and found_first_relative_layout
        ):
            break
    # print(", ".join(texts))
    gt = ", ".join(texts)
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
