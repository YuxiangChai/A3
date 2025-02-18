from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "In settings, hide Tasks, Events, and Birthdays, keeping only Holidays visible in google calendar.",
        "level": "medium",
        "category": "operation",
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
    Evaluates whether Tasks, Events, and Birthdays are hidden, and only Holidays remain checked
    by scanning all history XMLs.

    Args:
        xml (str): Current XML content as a string (not used here).
        screenshot (str): Base64 encoded screenshot string (not used here).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if any history XML satisfies the condition, False otherwise.
    """

    # Step 1: Define the expected labels and their states
    expected_content = [
        ("Events", "unchecked"),
        ("Tasks", "unchecked"),
        ("Birthdays", "unchecked"),
        ("Holiday", "checked"),
    ]

    # Step 2: Iterate over all history XMLs
    for idx, xml_data in enumerate(history.get("xml", [])):
        parser = ETParser(xml_data)

        # Step 3: Find all elements with resource-id "com.google.android.calendar:id/calendar_text"
        target_elements = []
        for el in parser.et.iter():
            if (
                el.attrib.get("resource-id")
                == "com.google.android.calendar:id/calendar_text"
            ):
                parent = parser.find_parent(el)  # Get parent element
                if parent is not None:
                    target_elements.append(parent)

        # Step 4: Check if exactly 4 parent elements are found
        if len(target_elements) != 4:
            # print(
            #     f"XML index {idx}: Expected 4 target elements, but found {len(target_elements)}."
            # )
            continue

        # Step 5: Validate the content-desc of the 4 parents in order
        eval_success = True
        for i, (label, status) in enumerate(expected_content):
            content_desc = target_elements[i].attrib.get("content-desc", "")

            # Match label and status
            if label in content_desc and status in content_desc:
                continue  # Matched correctly, proceed to next
            else:
                # print(
                #     f"XML index {idx}: Mismatch at element {i+1}. Expected '{label}, {status}', but got '{content_desc}'."
                # )
                eval_success = False
                break

        # Step 6: If all checks pass for this XML, return True
        if eval_success:
            # print(f"Condition satisfied in XML index {idx}.")
            return True

    # Step 7: If no XML meets the condition, return False
    # print(
    #     "No XML in history satisfies the condition: Tasks, Events, and Birthdays hidden, only Holidays checked."
    # )
    return False
