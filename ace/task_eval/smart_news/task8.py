# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> str:
    """
    Returns the task description.
    """
    return {
        "task": "Search for 'Trump' in SmartNews and retrieves the publishers of the top 3 news articles",
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
    """
    Verifies the search for 'Trump' in SmartNews and retrieves the publishers of the top 3 news articles.

    Args:
        xml (str): Current XML content.
        screenshot (str): Screenshot content (unused in this task).
        history (dict): History containing:
                        - "xml": List of XML file paths.

    Returns:
        list: A list containing the names of the top 3 publishers.
    """
    publishers = []
    search_found = False  # Flag to indicate if search for 'Trump' was detected

    try:
        # Step 1: Check if the search was performed in any historical XML
        for idx, xml_path in enumerate(history.get("xml", [])):
            parser = ETParser(xml_path)

            # Look for search confirmation
            search_element = parser.get_element(
                "resource-id", "jp.gocro.smartnews.android:id/search_src_text"
            )
            # print(search_element.attrib.get("text", "").strip())
            if search_element is not None:
                if search_element.attrib.get("text", "").strip() == "Trump":
                    search_found = True
                    break  # Stop checking other XML files once found

        if not search_found:
            # print("Search for 'Trump' was not performed in any XML files.")
            return False

        # Step 2: Extract publisher names from the current XML
        # parser = ETParser(xml)
        publisher_elements = [
            el.attrib.get("text", "").strip()
            for el in parser.et.iter()
            if el.attrib.get("resource-id", "")
            == "jp.gocro.smartnews.android:id/publisher"
        ]

        # Collect the top 3 publisher names
        publishers = publisher_elements[:3]
        # print(f"Top 3 Publishers: {publishers}")

    except Exception as e:
        # print(f"An error occurred during evaluation: {str(e)}")
        return False

    gt = f"Top 3 Publishers: {publishers}"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
