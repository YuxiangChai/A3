# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Retrieve the top 3 grocery names, ratings, and rating counts from the DoorDash charts",
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
    Retrieves the top 3 grocery names, their ratings, and rating counts from the DoorDash grocery charts.

    Args:
        xml (str): Current XML content (unused in this task).
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Historical XML content with keys:
                        - "xml": List of XML file paths.

    Returns:
        str: A formatted string containing the grocery names, their ratings, and rating counts.
    """
    grocery_list = []  # List to store top 3 grocery names
    grocery_data = {}  # Dictionary to store grocery_name: (rating, rating_count)

    # Step 1: Find the chart XML and extract the top 3 grocery names
    for idx, xml_content in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_content)

            # Check if this is the chart XML (contains text="Grocery")
            for el in parser.et.iter():
                if (
                    el.attrib.get("resource-id", "") == "com.dd.doordash:id/title"
                    and el.attrib.get("text", "") == "Grocery"
                ):
                    # Collect all grocery names (2nd to 4th elements)
                    titles = [
                        e.attrib.get("text", "").strip()
                        for e in parser.et.iter()
                        if e.attrib.get("resource-id", "") == "com.dd.doordash:id/title"
                    ]
                    if len(titles) >= 4:
                        grocery_list = titles[1:4]  # 2nd to 4th items
                    break
        except Exception as e:
            # print("Error processing XML file")
            continue

    if not grocery_list:
        return False

    # Step 2: Find grocery details (ratings and rating counts)
    for idx, xml_content in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_content)
            for el in parser.et.iter():
                # Match grocery name with store title
                if (
                    el.attrib.get("resource-id", "") == "com.dd.doordash:id/store_title"
                    and el.attrib.get("text", "") in grocery_list
                ):
                    grocery_name = el.attrib.get("text", "").strip()

                    # Extract average ratings and number of ratings
                    rating = None
                    rating_count = None
                    for e in parser.et.iter():
                        if (
                            e.attrib.get("resource-id", "")
                            == "com.dd.doordash:id/average_ratings"
                        ):
                            rating = e.attrib.get("text", "").strip()
                        elif (
                            e.attrib.get("resource-id", "")
                            == "com.dd.doordash:id/number_of_ratings"
                        ):
                            rating_count = e.attrib.get("text", "").strip()

                    if rating and rating_count:
                        grocery_data[grocery_name] = (rating, rating_count)
                    break
        except Exception as e:
            # print("Error processing XML file")
            continue

    # Step 3: Format the results
    result_strings = []
    for grocery in grocery_list:
        rating, rating_count = grocery_data.get(grocery, ("N/A", "N/A"))
        result_strings.append(f"{grocery}: {rating}; {rating_count}")
    final_result = ", ".join(result_strings)

    gt = final_result
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
