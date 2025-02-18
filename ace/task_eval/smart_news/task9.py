# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Retrieve the names of all sections in the SmartNews personalized news section.",
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
    Evaluates whether the names of all sections in the personalized news section
    of SmartNews can be retrieved.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: Always returns True after extracting the names, as the task is information retrieval.
    """
    # Initialize a list to store section names
    section_names = []

    # Step 1: Iterate through history XMLs to find the correct XML page
    for idx, xml_data in enumerate(history["xml"]):
        parser = ETParser(xml_data)

        # Check if the page is the "Personalize SmartNews" section
        personalize_element = None
        for el in parser.et.iter():
            if el.attrib.get("text") == "Personalize SmartNews":
                personalize_element = el
                break

        # If found, process this XML to retrieve the names
        if personalize_element:
            # print(f"Correct XML found at index {idx}. Extracting section names...")

            # Step 2: Collect all elements with resource-id="jp.gocro.smartnews.android:id/nameTextView"
            for el in parser.et.iter():
                if (
                    el.attrib.get("resource-id")
                    == "jp.gocro.smartnews.android:id/nameTextView"
                ):
                    name = el.attrib.get("text", "").strip()
                    if name:
                        section_names.append(name)

            # Step 3: Print the extracted section names
            # print("Section names in the personalized SmartNews section:")
            gt = ""
            for i, name in enumerate(section_names, start=1):
                gt += f"{i}. name: {name}\n"
            # Return True as the task is complete
            judge = answer_correct_judge(
                task,
                answer,
                gt,
                client,
                model_type,
            )
            return judge

    # If no valid XML was found in history
    # print("No valid 'Personalize SmartNews' XML found in history.")
    return False
