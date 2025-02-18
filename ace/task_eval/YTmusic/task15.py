import re

from ace.utils.common_utils import answer_correct_judge

# from a3.utils.xml_parser import ETParser
from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "In Youtube music, evaluates the top 3 songs from Taylor Swift's '1989' album with their comment counts, tell me which one is the highest",
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
    Evaluates the top 3 songs from Taylor Swift's '1989' album and retrieves their comment counts.

    Args:
        xml (str): Current XML content (unused in this task).
        screenshot (str): Screenshot content (unused in this task).
        history (dict): Historical XML content with keys:
                        - "xml": List of XML file paths.

    Returns:
        dict: A dictionary containing the comment counts for each song and the song with the most comments.
    """
    # Define the three target songs
    target_songs = {
        "Blank Space": "Blank Space",
        "Welcome To New York": "Welcome To New York (Taylor's Version) (Lyric Video)",
        "Style": "Style",
    }

    # Dictionary to store the comment counts for each song
    comment_counts = {song: 0 for song in target_songs}
    most_commented_song = None
    max_comments = 0

    # Iterate through each XML in the history
    for idx, xml_content in enumerate(history.get("xml", [])):
        try:
            parser = ETParser(xml_content)

            # Step 1: Check for each song title
            for song, title in target_songs.items():
                title_element = parser.get_element(
                    "resource-id", "com.google.android.apps.youtube.music:id/title"
                )
                if (
                    title_element is not None
                    and title_element.attrib.get("text", "").strip() == title
                ):
                    # print(
                    #     f"[{idx}] Found song '{song}' in the XML. Searching for comments..."
                    # )

                    # Step 2: Traverse all elements and filter valid content-desc
                    for element in parser.et.iter():
                        content_desc = element.attrib.get("content-desc", "").strip()
                        if content_desc.startswith("View") and content_desc.endswith(
                            "comments"
                        ):
                            # Match "View X comments" and extract the number
                            match = re.search(r"View ([\d,]+) comments", content_desc)
                            # print(content_desc)
                            if match:
                                comment_count = int(match.group(1).replace(",", ""))
                                comment_counts[song] = comment_count
                                # print(f"[{idx}] '{song}' has {comment_count} comments.")

                                # Update the most commented song
                                if comment_count > max_comments:
                                    max_comments = comment_count
                                    most_commented_song = song
                    break  # No need to continue checking other titles in this file

        except FileNotFoundError:
            # print("Error: File not found. Skipping...")
            pass
        except Exception as e:
            # print("Error processing XML file")
            pass

    # Summary of results
    # print("Final Comment Counts:")
    # for song, count in comment_counts.items():
    #     print(f"- {song}: {count} comments")

    # if most_commented_song:
    #     print(
    #         f"The song with the most comments is '{most_commented_song}' with {max_comments} comments."
    #     )
    # else:
    #     print("No comments found for any of the songs.")

    gt = f"The song with the most comments is '{most_commented_song}' with {max_comments} comments."
    # Return results
    judge = answer_correct_judge(
        task,
        answer,
        gt,
        client,
        model_type,
    )
    return judge
