from ace.utils.xml_parser import ETParser


def task() -> dict:
    """
    Returns the task details as a dictionary.
    """
    return {
        "task": "Add a task titled 'Go to the market' on November 9 at 1:30 PM to Google Calendar.",
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
    Evaluates whether the task titled 'Go to the market' has been successfully added to Google Calendar.

    Args:
        xml (str): Current XML content as a string.
        screenshot (str): Base64 encoded screenshot string (optional).
        history (dict): Historical context with XMLs and actions.

    Returns:
        bool: True if the task has been successfully added, False otherwise.
    """

    title_found = False
    task_checked = False
    save_action_verified = False

    # Step 1: Iterate through all history XMLs to validate conditions 1 and 2
    for idx, xml_data in enumerate(history["xml"]):
        parser = ETParser(xml_data)

        # Condition 1: Check title "Go to the market"
        title_element = parser.get_element(
            "resource-id", "com.google.android.calendar:id/title"
        )
        if (
            title_element is not None
            and title_element.attrib.get("text", "").strip() == "Go to the market"
        ):
            title_found = True

            # Condition 2: Check if an element with text="Task" exists and has checked="true"
            task_element = parser.get_element("text", "Task")
            if (
                task_element is not None
                and task_element.attrib.get("checked", "").lower() == "true"
            ):
                task_checked = True
            # content-desc="New task: gogo, Saturday, November 9, 1:30 PM – 2:00 PM"

            # Condition 3: Check if an element with correct time
            task_element = parser.get_element(
                "content-desc",
                "New task: Go to the market, Saturday, November 9, 1:30 PM – 2:00 PM",
            )
            if task_element is not None:
                task_checked = True

                # Step 2: Check action[-2] for "tap" in the save button bounds
                try:
                    save_button_element = parser.get_element(
                        "resource-id", "com.google.android.calendar:id/save"
                    )
                    if save_button_element is not None:
                        save_bounds = save_button_element.attrib.get("bounds", "")
                        if not save_bounds:
                            # print(
                            #     f"Save button bounds not found in XML at index {idx}."
                            # )
                            continue

                        # Parse bounds string to get coordinates
                        bounds = save_bounds.strip("[]").split("][")
                        x1, y1 = map(int, bounds[0].split(","))
                        x2, y2 = map(int, bounds[1].split(","))

                        # Retrieve action[-2] from history
                        save_action = history["actions"][-2]
                        if (
                            save_action["action"] == "tap"
                            and x1 <= save_action["x"] <= x2
                            and y1 <= save_action["y"] <= y2
                        ):
                            save_action_verified = True
                            break
                except (KeyError, IndexError, ValueError) as e:
                    continue

    # Step 3: Final validation
    if title_found and task_checked and save_action_verified:
        return True

    # Print failure reasons for debugging
    # if not title_found:
    #     print("Title 'Go to the market' not found in any history XML.")
    # if not task_checked:
    #     print("Element 'Task' is not checked (checked='true').")
    # if not save_action_verified:
    #     print("Save action was not performed correctly.")

    return False
