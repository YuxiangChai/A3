# from ace.utils.avd_control import Controller
# from ace.utils.xml_parser import ETParser


# def pre_task(controller: Controller) -> None:
#     from time import sleep

#     action = {"action": "open", "app": "coursera"}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(3)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     srch_button = parser.get_element("content-desc", "Search")
#     srch_button_bounds = parser.get_bounds(srch_button)
#     srch_button_x = (srch_button_bounds[0] + srch_button_bounds[2]) // 2
#     srch_button_y = (srch_button_bounds[1] + srch_button_bounds[3]) // 2
#     action = {"action": "tap", "x": srch_button_x, "y": srch_button_y}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(2)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     srch_bar_button = parser.get_element("class", "android.widget.EditText")
#     srch_bar_button_bounds = parser.get_bounds(srch_bar_button)
#     srch_bar_button_x = (srch_bar_button_bounds[0] + srch_bar_button_bounds[2]) // 2
#     srch_bar_button_y = (srch_bar_button_bounds[1] + srch_bar_button_bounds[3]) // 2
#     action = {"action": "tap", "x": srch_bar_button_x, "y": srch_bar_button_y}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(2)

#     action = {"action": "type", "text": "cryptography"}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(2)

#     action = {"action": "enter"}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(2)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     first_course_element = parser.get_element_contains("text", "Course")
#     first_course_button = parser.find_clickable_parent(first_course_element)
#     first_course_button_bounds = parser.get_bounds(first_course_button)
#     first_course_button_x = (
#         first_course_button_bounds[0] + first_course_button_bounds[2]
#     ) // 2
#     first_course_button_y = (
#         first_course_button_bounds[1] + first_course_button_bounds[3]
#     ) // 2
#     action = {"action": "tap", "x": first_course_button_x, "y": first_course_button_y}

#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(2)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     enroll_element = parser.get_element("text", "See enrollment options")
#     if enroll_element is not None:
#         enroll_button = parser.find_clickable_parent(enroll_element)
#         enroll_button_bounds = parser.get_bounds(enroll_button)
#         enroll_button_x = (enroll_button_bounds[0] + enroll_button_bounds[2]) // 2
#         enroll_button_y = (enroll_button_bounds[1] + enroll_button_bounds[3]) // 2
#         action = {"action": "tap", "x": enroll_button_x, "y": enroll_button_y}

#         controller.exe_action(action, False)
#         # wait for execution fully completed
#         sleep(5)

#         xml = controller._get_xml()
#         parser = ETParser(xml)

#         enroll_wo_certificate_element = parser.get_element(
#             "text", "Enroll without Certificate"
#         )
#         enroll_wo_certificate_button = parser.find_clickable_parent(
#             enroll_wo_certificate_element
#         )
#         enroll_wo_certificate_button_bounds = parser.get_bounds(
#             enroll_wo_certificate_button
#         )
#         enroll_wo_certificate_button_x = (
#             enroll_wo_certificate_button_bounds[0]
#             + enroll_wo_certificate_button_bounds[2]
#         ) // 2
#         enroll_wo_certificate_button_y = (
#             enroll_wo_certificate_button_bounds[1]
#             + enroll_wo_certificate_button_bounds[3]
#         ) // 2
#         action = {
#             "action": "tap",
#             "x": enroll_wo_certificate_button_x,
#             "y": enroll_wo_certificate_button_y,
#         }

#         controller.exe_action(action, False)
#         sleep(2)

#         enroll2_button = parser.get_element_contains_from(
#             "class", "android.view.View", "text", "Enroll without Certificate"
#         )
#         enroll2_button_bounds = parser.get_bounds(enroll2_button)
#         enroll2_button_x = (enroll2_button_bounds[0] + enroll2_button_bounds[2]) // 2
#         enroll2_button_y = (enroll2_button_bounds[1] + enroll2_button_bounds[3]) // 2
#         action = {"action": "tap", "x": enroll2_button_x, "y": enroll2_button_y}

#         controller.exe_action(action, False)
#         sleep(2)

#     action = {"action": "home"}
#     controller.exe_action(action, False)
#     sleep(1)

#     action = {"action": "end"}
#     controller.exe_action(action, False)
