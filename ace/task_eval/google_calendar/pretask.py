# import time

# from ace.utils.avd_control import Controller
# from ace.utils.xml_parser import ETParser


# def pre_task(controller: Controller) -> None:
#     """
#     Pre-task initialization for Google Calendar.
#     Pre-adds an event titled 'watch football game' to the calendar.

#     Args:
#         controller: The Controller instance for executing actions and retrieving XML.
#     """
#     # Step 1: Open the Google Calendar app
#     controller._open("google_calendar")
#     time.sleep(3)

#     # Step 2: Tap the 'Add Plan' button
#     xml1 = controller._get_xml()
#     parser = ETParser(xml1)
#     add_plan_button = parser.get_element(
#         "resource-id", "com.google.android.calendar:id/floating_action_button"
#     )

#     if add_plan_button is None:
#         return

#     add_plan_bounds = add_plan_button.attrib.get("bounds", "")
#     if not add_plan_bounds:
#         return

#     x1, y1, x2, y2 = map(int, add_plan_bounds.strip("[]").replace("][", ",").split(","))
#     tap_x, tap_y = (x1 + x2) // 2, (y1 + y2) // 2
#     controller._tap(tap_x, tap_y)
#     time.sleep(2)

#     # Step 3: Select 'Event'
#     xml2 = controller._get_xml()
#     parser = ETParser(xml2)
#     event_button = parser.get_element(
#         "resource-id", "com.google.android.calendar:id/speed_dial_icon"
#     )

#     if event_button is None:
#         return

#     event_bounds = event_button.attrib.get("bounds", "")
#     if event_bounds is None:
#         return

#     x1, y1, x2, y2 = map(int, event_bounds.strip("[]").replace("][", ",").split(","))
#     tap_x, tap_y = (x1 + x2) // 2, (y1 + y2) // 2
#     controller._tap(tap_x, tap_y)
#     time.sleep(2)

#     # Step 4: Input event title
#     controller._type("watch football game")
#     time.sleep(2)

#     # Validate the title
#     xml3 = controller._get_xml()
#     parser = ETParser(xml3)
#     # title_element = parser.get_element(
#     #     "resource-id", "com.google.android.calendar:id/title"
#     # )

#     # if (
#     #     title_element is None
#     #     or title_element.attrib.get("text", "") != "Watch football game"
#     # ):
#     #     return

#     # Step 5: Save the event
#     save_button = parser.get_element(
#         "resource-id", "com.google.android.calendar:id/save"
#     )

#     if save_button is None:
#         print("no save button")
#         return

#     save_bounds = save_button.attrib.get("bounds", "")
#     if save_bounds is None:
#         return

#     x1, y1, x2, y2 = map(int, save_bounds.strip("[]").replace("][", ",").split(","))
#     tap_x, tap_y = (x1 + x2) // 2, (y1 + y2) // 2
#     controller._tap(tap_x, tap_y)
