# from ace.utils.avd_control import Controller
# from ace.utils.xml_parser import ETParser


# def pre_task(controller: Controller) -> None:
#     from time import sleep

#     action = {"action": "open", "app": "GoogleTasks"}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(3)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     # find list bar element
#     list_bar = parser.get_element(
#         "resource-id", "com.google.android.apps.tasks:id/tabs"
#     )
#     list_bar_bounds = parser.get_bounds(list_bar)
#     list_bar_y = (list_bar_bounds[3] + list_bar_bounds[1]) // 2

#     # 滑动找到新建list按钮
#     new_list = None
#     action = {
#         "action": "swipe",
#         "x1": list_bar_bounds[2] - 100,
#         "y1": list_bar_y,
#         "x2": list_bar_bounds[0] + 100,
#         "y2": list_bar_y,
#     }
#     while new_list is None:
#         controller.exe_action(action, False)
#         # wait for execution fully completed
#         sleep(2)

#         xml = controller._get_xml()
#         parser = ETParser(xml)
#         new_list = parser.get_element("text", "New list")

#     # find the new list button
#     new_list_bounds = parser.get_bounds(new_list)
#     new_list_x = (new_list_bounds[2] + new_list_bounds[0]) // 2
#     new_list_y = (new_list_bounds[3] + new_list_bounds[1]) // 2

#     # tap the button
#     action = {"action": "tap", "x": new_list_x, "y": new_list_y}
#     controller.exe_action(action, False)
#     sleep(2)

#     # type Homework
#     action = {"action": "type", "text": "Homework"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # enter
#     action = {"action": "enter"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # Home
#     action = {"action": "home"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # end
#     action = {"action": "end"}
#     controller.exe_action(action, False)

#     sleep(2)
#     controller._terminate_all_apps()

#     action = {"action": "open", "app": "GoogleTasks"}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(3)
#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     list_bar = parser.get_element(
#         "resource-id", "com.google.android.apps.tasks:id/tabs"
#     )
#     list_bar_bounds = parser.get_bounds(list_bar)
#     list_bar_y = (list_bar_bounds[3] + list_bar_bounds[1]) // 2

#     # 滑动找到homework按钮
#     action = {
#         "action": "swipe",
#         "x1": list_bar_bounds[2] - 300,
#         "y1": list_bar_y,
#         "x2": list_bar_bounds[0] + 300,
#         "y2": list_bar_y,
#     }

#     # whether in Homework list
#     homework_list = parser.get_element_bydic(
#         {
#             "text": "Homework",
#             "resource-id": "com.google.android.apps.tasks:id/task_list_title",
#         }
#     )
#     if homework_list is None:
#         homework_element = parser.get_element("text", "Homework")
#         while homework_element is None:
#             controller.exe_action(action, False)
#             # wait for execution fully completed
#             sleep(2)
#             xml = controller._get_xml()
#             parser = ETParser(xml)
#             homework_element = parser.get_element("text", "Homework")
#         homework_button = parser.find_clickable_parent(homework_element)
#         homework_button_bounds = parser.get_bounds(homework_button)
#         homework_button_x = (homework_button_bounds[2] + homework_button_bounds[0]) // 2
#         homework_button_y = (homework_button_bounds[3] + homework_button_bounds[1]) // 2

#         # go into homework list
#         action = {"action": "tap", "x": homework_button_x, "y": homework_button_y}
#         controller.exe_action(action, False)
#         # wait for execution fully completed
#         sleep(2)
#         xml = controller._get_xml()
#         parser = ETParser(xml)

#     # add task
#     add_task_element = parser.get_element("content-desc", "Create new task")
#     add_task_button = parser.find_clickable_parent(add_task_element)
#     add_task_button_bounds = parser.get_bounds(add_task_button)
#     add_task_button_x = (add_task_button_bounds[2] + add_task_button_bounds[0]) // 2
#     add_task_button_y = (add_task_button_bounds[3] + add_task_button_bounds[1]) // 2
#     action = {"action": "tap", "x": add_task_button_x, "y": add_task_button_y}
#     controller.exe_action(action, False)
#     sleep(2)

#     # type name
#     action = {"action": "type", "text": "Python Assignment1"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # enter
#     action = {"action": "enter"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # Home
#     action = {"action": "home"}
#     controller.exe_action(action, False)
#     sleep(1)

#     controller._terminate_all_apps()

#     action = {"action": "open", "app": "GoogleTasks"}
#     controller.exe_action(action, False)
#     # wait for execution fully completed
#     sleep(3)

#     xml = controller._get_xml()
#     parser = ETParser(xml)

#     # find list bar element
#     list_bar = parser.get_element(
#         "resource-id", "com.google.android.apps.tasks:id/tabs"
#     )
#     list_bar_bounds = parser.get_bounds(list_bar)
#     list_bar_y = (list_bar_bounds[3] + list_bar_bounds[1]) // 2

#     # 滑动找到新建list按钮
#     new_list = None
#     action = {
#         "action": "swipe",
#         "x1": list_bar_bounds[2] - 100,
#         "y1": list_bar_y,
#         "x2": list_bar_bounds[0] + 100,
#         "y2": list_bar_y,
#     }
#     while new_list is None:
#         controller.exe_action(action, False)
#         # wait for execution fully completed
#         sleep(2)

#         xml = controller._get_xml()
#         parser = ETParser(xml)
#         new_list = parser.get_element("text", "New list")

#     # find the new list button
#     new_list_bounds = parser.get_bounds(new_list)
#     new_list_x = (new_list_bounds[2] + new_list_bounds[0]) // 2
#     new_list_y = (new_list_bounds[3] + new_list_bounds[1]) // 2

#     # tap the button
#     action = {"action": "tap", "x": new_list_x, "y": new_list_y}
#     controller.exe_action(action, False)
#     sleep(2)

#     # type Math homework
#     action = {"action": "type", "text": "Math homework"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # enter
#     action = {"action": "enter"}
#     controller.exe_action(action, False)
#     sleep(2)
#     xml = controller._get_xml()
#     parser = ETParser(xml)
#     new_list = parser.get_element("text", "New list")

#     # find the new list button
#     new_list_bounds = parser.get_bounds(new_list)
#     new_list_x = (new_list_bounds[2] + new_list_bounds[0]) // 2
#     new_list_y = (new_list_bounds[3] + new_list_bounds[1]) // 2

#     # tap the button
#     action = {"action": "tap", "x": new_list_x, "y": new_list_y}
#     controller.exe_action(action, False)
#     sleep(2)

#     # type English homework
#     action = {"action": "type", "text": "English homework"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # enter
#     action = {"action": "enter"}
#     controller.exe_action(action, False)
#     sleep(2)
#     xml = controller._get_xml()
#     parser = ETParser(xml)
#     new_list = parser.get_element("text", "New list")

#     # find the new list button
#     new_list_bounds = parser.get_bounds(new_list)
#     new_list_x = (new_list_bounds[2] + new_list_bounds[0]) // 2
#     new_list_y = (new_list_bounds[3] + new_list_bounds[1]) // 2

#     # tap the button
#     action = {"action": "tap", "x": new_list_x, "y": new_list_y}
#     controller.exe_action(action, False)
#     sleep(2)

#     # type History homework
#     action = {"action": "type", "text": "History homework"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # enter
#     action = {"action": "enter"}
#     controller.exe_action(action, False)
#     sleep(2)

#     # home
#     action = {"action": "home"}
#     controller.exe_action(action, False)
#     sleep(1)
