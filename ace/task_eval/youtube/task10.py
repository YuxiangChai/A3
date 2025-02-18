# from a3.utils.xml_parser import ETParser
from ace.utils.common_utils import answer_correct_judge
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Get the latest video titles of the top 3 YouTubers from the subscriptions page",
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
    Retrieves the latest video information for the top 3 YouTubers from the subscription page.

    Args:
        xml (str): Current XML content (unused in this task).
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Historical XML content with keys:
                        - "xml": List of XML file paths.

    Returns:
        dict: A dictionary containing the latest video titles for the top 3 YouTubers.
    """
    top_youtubers = []  # List to store the top 3 YouTuber names
    latest_videos = {}  # Dictionary to store video info {author: video_title}

    # Step 1: Identify the subscription page and extract the top 3 YouTubers
    for idx, xml_content in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_content)

            # Extract all content-desc values
            content_desc_list = [
                el.attrib.get("content-desc", "").strip()
                for el in parser.et.iter()
                if "content-desc" in el.attrib
            ]

            # Check if this XML is a subscription page (contains >=2 "Options")
            options_indices = [
                i for i, val in enumerate(content_desc_list) if val == "Options"
            ]
            if len(options_indices) >= 3:  # Ensure at least 3 "Options" exist
                # Extract the YouTuber names: "Options" 前面的 content-desc 是作者名称
                for i in options_indices[:3]:
                    author_name = content_desc_list[i - 1]
                    if author_name and author_name not in top_youtubers:
                        top_youtubers.append(author_name)
                break  # Stop after finding the subscription page

        except Exception as e:
            # print("Error processing XML file")
            continue

    if not top_youtubers:
        # print("No subscription page found. Exiting...")
        return False

    # Step 2: Search for video lists for the top 3 YouTubers
    for idx, xml_content in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_content)

            # Iterate over all elements to find text matching a YouTuber
            for element in parser.et.iter():
                title_text = element.attrib.get("text", "").strip()
                if title_text in top_youtubers:
                    # Extract all content-desc values
                    content_desc_list = [
                        el.attrib.get("content-desc", "").strip()
                        for el in parser.et.iter()
                        if "content-desc" in el.attrib
                    ]

                    # Find the first "Action menu" and get the video title before it
                    for i, val in enumerate(content_desc_list):
                        if val == "Action menu" and i > 0:
                            video_title = content_desc_list[i - 1]
                            latest_videos[title_text] = video_title
                            break
                    break  # Stop after processing this YouTuber's page

        except Exception as e:
            # print("Error processing XML file")
            continue

    # Step 3: Return the results
    # print("Final Latest Videos:")

    gt = ""
    for i, (author, video) in enumerate(latest_videos.items(), start=1):
        gt += f"{i}. {author}: {video}\n"
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
