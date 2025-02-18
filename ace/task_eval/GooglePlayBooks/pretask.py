# from ace.utils.avd_control import Controller
# from ace.utils.xml_parser import ETParser


# def pre_task(controller: Controller) -> None:
#     from time import sleep

#     action = {"action": "open", "app": "GooglePlayBooks"}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(3)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     srch_bar_button = parser.get_element("text", "Search Play Books")
#     srch_bar_button_bounds = parser.get_bounds(srch_bar_button)
#     srch_bar_button_x = (srch_bar_button_bounds[0] + srch_bar_button_bounds[2]) // 2
#     srch_bar_button_y = (srch_bar_button_bounds[1] + srch_bar_button_bounds[3]) // 2
#     action = {"action": "tap", "x": srch_bar_button_x, "y": srch_bar_button_y}
#     controller.exe_action(action, False)
#     sleep(2)

#     action = {"action": "type", "text": "Hemingway's In Our Time"}
#     controller.exe_action(action, False)
#     sleep(2)

#     action = {"action": "enter"}
#     controller.exe_action(action, False)
#     sleep(2)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     first_book_button = parser.get_element(
#         "resource-id",
#         "com.google.android.apps.books:id/card_image_body_button_list_item_root",
#     )
#     first_book_button_bounds = parser.get_bounds(first_book_button)
#     first_book_button_x = (
#         first_book_button_bounds[0] + first_book_button_bounds[2]
#     ) // 2
#     first_book_button_y = (
#         first_book_button_bounds[1] + first_book_button_bounds[3]
#     ) // 2
#     action = {"action": "tap", "x": first_book_button_x, "y": first_book_button_y}

#     controller.exe_action(action, False)
#     sleep(2)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     wishlist_button = parser.get_element("content-desc", "Add to wishlist")
#     if wishlist_button is not None:
#         wishlist_button_bounds = parser.get_bounds(wishlist_button)
#         wishlist_button_x = (wishlist_button_bounds[0] + wishlist_button_bounds[2]) // 2
#         wishlist_button_y = (wishlist_button_bounds[1] + wishlist_button_bounds[3]) // 2
#         action = {"action": "tap", "x": wishlist_button_x, "y": wishlist_button_y}
#         controller.exe_action(action, False)
#         sleep(2)

#     action = {"action": "home"}
#     controller.exe_action(action, False)
#     sleep(1)

#     action = {"action": "end"}
#     controller.exe_action(action, False)

#     return
