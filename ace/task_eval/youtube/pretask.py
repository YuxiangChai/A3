# import subprocess
# import time

# from ace.utils.avd_control import Controller
# from ace.utils.xml_parser import ETParser


# def pre_task(controller: Controller) -> None:
#     """
#     Pre-task initialization for the task.
#     Opens the YouTube app, navigates to the Shorts section, and subscribes to YouTubers.
#     """
#     # Open YouTube app
#     # controller._open("youtube")
#     subprocess.run(
#         [
#             "adb",
#             "shell",
#             "monkey",
#             "-p",
#             "com.google.android.youtube",
#             "-c",
#             "android.intent.category.LAUNCHER",
#             "1",
#         ],
#         stdout=subprocess.DEVNULL,  # Suppress stdout
#         stderr=subprocess.DEVNULL,  # Suppress stderr
#     )
#     # print("Opening YouTube...")
#     time.sleep(3)

#     # Step 1: Navigate to Shorts section
#     xml = controller._get_xml()
#     parser = ETParser(xml)
#     shorts_element = parser.get_element("content-desc", "Shorts")

#     if shorts_element is None:
#         # print("Failed to find 'Shorts' element in the current XML.")
#         return

#     # Check if Shorts is already selected
#     if shorts_element.attrib.get("selected", "").lower() != "true":
#         # Tap on Shorts to navigate to the Shorts section
#         bounds = shorts_element.attrib.get("bounds", "")
#         if bounds:
#             coords = bounds.strip("[]").split("][")
#             x1, y1 = map(int, coords[0].split(","))
#             x2, y2 = map(int, coords[1].split(","))
#             tap_x = (x1 + x2) // 2
#             tap_y = (y1 + y2) // 2
#             # print(f"Tapping on Shorts at ({tap_x}, {tap_y})...")
#             controller._tap(tap_x, tap_y)
#             time.sleep(2)
#         else:
#             # print("Bounds for 'Shorts' element not found.")
#             return
#     else:
#         # print("'Shorts' is already selected.")
#         pass

#     # Step 2: Subscribe to YouTubers in the Shorts section
#     subscribed_count = 0
#     max_subscribe_count = 3

#     while subscribed_count < max_subscribe_count:
#         xml = controller._get_xml()
#         parser = ETParser(xml)

#         # Find the first "Subscribe to ..." button
#         subscribe_element = None
#         for el in parser.et.iter():
#             content_desc = el.attrib.get("content-desc", "")
#             if content_desc.startswith("Subscribe to"):
#                 subscribe_element = el
#                 break

#         if subscribe_element is not None:
#             # Tap on the Subscribe button
#             bounds = subscribe_element.attrib.get("bounds", "")
#             if bounds:
#                 coords = bounds.strip("[]").split("][")
#                 x1, y1 = map(int, coords[0].split(","))
#                 x2, y2 = map(int, coords[1].split(","))
#                 tap_x = (x1 + x2) // 2
#                 tap_y = (y1 + y2) // 2
#                 # print(f"Subscribing to YouTuber at ({tap_x}, {tap_y})...")
#                 controller._tap(tap_x, tap_y)
#                 subscribed_count += 1
#                 time.sleep(2)
#             else:
#                 # print("Bounds for 'Subscribe' element not found.")
#                 pass
#         else:
#             # Swipe to load the next video if no Subscribe button is found
#             # print("No 'Subscribe to' element found. Swiping to the next video...")
#             controller._swipe(
#                 controller.w // 2,
#                 controller.h // 2,
#                 controller.w // 2,
#                 controller.h // 4,
#             )
#             time.sleep(2)

#     # print(f"Subscribed to {subscribed_count} YouTubers.")
#     # print("Pre-task initialization for YouTube completed.")
