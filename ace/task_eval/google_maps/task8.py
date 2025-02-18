# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Search for 'cafe' in Google Maps and tell me the store names sorted by both Distance and Relevance",
        "level": "medium",
        "category": "multi-page query",
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
    """
    Search for 'cafe' in Google Maps and retrieve store names for both Distance and Relevance sorting.

    Args:
        xml (str): Current XML content (unused in this task).
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Historical XML content with keys:
                        - "xml": List of XML file paths.

    Returns:
        str: A formatted string containing the store names for Distance and Relevance sorting.
    """
    # Use sets to store results and avoid duplicates
    distance_stores = set()
    relevance_stores = set()

    # Iterate through each XML file in the history
    for idx, xml_path in enumerate(history.get("xml", [])):
        try:
            # print(f"Processing XML file: {xml_path}")
            with open(xml_path, "r", encoding="utf-8") as file:
                xml_content = file.read()
            parser = ETParser(xml_content)

            # Step 1: Check if "caffee" appears in text
            found_caffee = any(
                el.attrib.get("text", "") == "cafe" for el in parser.et.iter()
            )
            if not found_caffee:
                continue

            # Step 2: Check sorting method and store name
            current_sort_method = None
            for el in parser.et.iter():
                text = el.attrib.get("text", "").strip()
                content_desc = el.attrib.get("content-desc", "").strip()

                if text == "Relevance" and content_desc == "Relevance":
                    current_sort_method = "Relevance"
                elif text == "Distance" and content_desc == "Distance":
                    current_sort_method = "Distance"

                # If sorting method is detected, find the store name
                if current_sort_method:
                    for el_store in parser.et.iter():
                        if (
                            el_store.attrib.get("resource-id", "")
                            == "com.google.android.apps.maps:id/title"
                        ):
                            store_name = el_store.attrib.get("text", "").strip()
                            if current_sort_method == "Distance":
                                distance_stores.add(store_name)
                            elif current_sort_method == "Relevance":
                                relevance_stores.add(store_name)
                            break

        except Exception as e:
            # print(f"[{idx}] Error processing XML file '{xml_path}': {str(e)}")
            continue

    # Final results processing
    distance_result = list(distance_stores)[0] if distance_stores else "None"
    relevance_result = list(relevance_stores)[0] if relevance_stores else "None"

    # Combine results into a formatted string
    final_result = f"By distance:{distance_result} By relevance:{relevance_result}"
    gt = final_result
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
