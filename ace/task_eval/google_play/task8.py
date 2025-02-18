import re

from ace.utils.common_utils import answer_correct_judge

# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Retrieve the download counts of the top 3 paid apps from the Google Play charts",
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
    Retrieves the top 3 paid apps and their download counts from Google Play charts.

    Args:
        xml (str): Current XML content (unused in this task).
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Historical XML content with keys:
                        - "xml": List of XML file paths.

    Returns:
        str: A formatted string containing the app names and their download counts.
    """
    top_apps = []  # List to store top 3 app names
    download_counts = {}  # Dictionary to store app name: download count mapping

    # Step 1: Find the chart XML and extract top 3 app names
    for idx, xml_content in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_content)

            # Check if this XML is the chart XML (contains "Top paid")
            if any(
                el.attrib.get("content-desc", "") == "Top paid"
                for el in parser.et.iter()
            ):
                # Extract all content-desc values
                content_desc_list = [
                    el.attrib.get("content-desc", "").strip()
                    for el in parser.et.iter()
                    if "content-desc" in el.attrib
                ]

                # The 3rd to 5th content-desc correspond to the top 3 apps
                for i in range(2, 5):  # Index 2-4 in the list (0-based index)
                    if i < len(content_desc_list):
                        app_info = content_desc_list[i]
                        app_name = app_info.split("\n")[
                            0
                        ]  # Split and get the first part
                        top_apps.append(app_name)
                break  # Stop after processing the chart XML
        except Exception as e:
            # print("Error processing XML file")
            continue

    if not top_apps:
        gt = "None"

    # Step 2: Find the download counts for the top 3 apps
    for idx, xml_content in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_content)

            # Check if the XML matches any app name in the top_apps list
            for el in parser.et.iter():
                if el.attrib.get("text", "").strip() in top_apps:
                    app_name = el.attrib.get("text", "").strip()

                    # Search for download count in content-desc
                    for el_desc in parser.et.iter():
                        content_desc = el_desc.attrib.get("content-desc", "").strip()
                        if content_desc.startswith(
                            "Downloaded"
                        ) and content_desc.endswith("times"):
                            download_count = re.search(
                                r"Downloaded (.+?) times", content_desc
                            )
                            if download_count:
                                download_counts[app_name] = download_count.group(1)
                                # print(
                                #     f"[{idx}] {app_name} Download Count: {download_count.group(1)}"
                                # )
                    break  # Stop searching this XML file
        except Exception as e:
            # print("Error processing XML file")
            continue

    # Step 3: Format the results
    result_strings = []
    for i, app_name in enumerate(top_apps):
        download_count = download_counts.get(app_name, "N/A")
        result_strings.append(f"{i+1}. {app_name}: {download_count}")
    final_result = ", ".join(result_strings)

    # print("\nFinal Result:")
    gt = final_result
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
