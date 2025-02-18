from ace.utils.avd_control import Controller
from ace.utils.xml_parser import ETParser


def pre_task(controller: Controller) -> None:
    from time import sleep

    action = {"action": "open", "app": "Instagram"}
    controller.exe_action(action, False)
    # wait for execution fully completed
    sleep(3)

    xml = controller._get_xml()
    parser = ETParser(xml)

    explore_element = parser.get_element("content-desc", "Search and explore")
    explore_button = parser.find_clickable_parent(explore_element)
    explore_button_bounds = parser.get_bounds(explore_button)

    explore_button_bounds_x = (explore_button_bounds[0] + explore_button_bounds[2]) // 2
    explore_button_bounds_y = (explore_button_bounds[1] + explore_button_bounds[3]) // 2

    action = {
        "action": "tap",
        "x": explore_button_bounds_x,
        "y": explore_button_bounds_y,
    }

    # click explore button
    controller.exe_action(action, False)
    # wait for execution fully completed
    sleep(2)

    xml = controller._get_xml()
    parser = ETParser(xml)

    srch_bar_element = parser.get_element(
        "resource-id", "com.instagram.android:id/action_bar_search_edit_text"
    )
    srch_bar_button = parser.find_clickable_parent(srch_bar_element)
    srch_bar_button_bounds = parser.get_bounds(srch_bar_button)

    srch_bar_button_bounds_x = (
        srch_bar_button_bounds[0] + srch_bar_button_bounds[2]
    ) // 2
    srch_bar_button_bounds_y = (
        srch_bar_button_bounds[1] + srch_bar_button_bounds[3]
    ) // 2

    action = {
        "action": "tap",
        "x": srch_bar_button_bounds_x,
        "y": srch_bar_button_bounds_y,
    }

    # click explore button
    controller.exe_action(action, False)
    sleep(2)

    action = {"action": "type", "text": "Taylorswift"}
    controller.exe_action(action, False)
    sleep(2)

    action = {"action": "enter"}
    controller.exe_action(action, False)
    sleep(2)
    xml = controller._get_xml()
    parser = ETParser(xml)

    # click accounts button
    accounts_element = parser.get_element_bydic(
        {"text": "Accounts", "class": "android.widget.TabWidget"}
    )
    accounts_button = parser.find_clickable_parent(accounts_element)
    accounts_button_bounds = parser.get_bounds(accounts_button)
    accounts_button_x = (accounts_button_bounds[0] + accounts_button_bounds[2]) // 2
    accounts_button_y = (accounts_button_bounds[1] + accounts_button_bounds[3]) // 2
    action = {"action": "tap", "x": accounts_button_x, "y": accounts_button_y}
    controller.exe_action(action, False)
    sleep(2)
    xml = controller._get_xml()
    parser = ETParser(xml)

    first_account_element = parser.get_element(
        "resource-id", "com.instagram.android:id/row_search_user_container"
    )
    first_account_button = parser.find_clickable_parent(first_account_element)
    first_account_button_bounds = parser.get_bounds(first_account_button)

    first_account_button_x = (
        first_account_button_bounds[0] + first_account_button_bounds[2]
    ) // 2
    first_account_button_y = (
        first_account_button_bounds[1] + first_account_button_bounds[3]
    ) // 2

    action = {"action": "tap", "x": first_account_button_x, "y": first_account_button_y}

    controller.exe_action(action, False)
    sleep(3)

    xml = controller._get_xml()
    parser = ETParser(xml)

    follow_button = parser.get_element(
        "resource-id", "com.instagram.android:id/profile_header_follow_button"
    )
    if follow_button.attrib["text"] == "Follow":
        follow_button_bounds = parser.get_bounds(follow_button)
        follow_button_x = (follow_button_bounds[0] + follow_button_bounds[2]) // 2
        follow_button_y = (follow_button_bounds[1] + follow_button_bounds[3]) // 2
        action = {"action": "tap", "x": follow_button_x, "y": follow_button_y}
        controller.exe_action(action, False)
        sleep(2)

    action = {"action": "home"}
    controller.exe_action(action, False)
    sleep(2)

    # controller._terminate_all_apps()

    # action = {"action": "open", "app": "Instagram"}
    # controller.exe_action(action, False)
    # # wait for execution fully completed
    # sleep(3)

    # xml = controller._get_xml()
    # parser = ETParser(xml)

    # create_button = parser.get_element("content-desc", "Create")
    # create_button_bounds = parser.get_bounds(create_button)
    # create_button_x = (create_button_bounds[0] + create_button_bounds[2]) // 2
    # create_button_y = (create_button_bounds[1] + create_button_bounds[3]) // 2
    # action = {"action": "tap", "x": create_button_x, "y": create_button_y}

    # controller.exe_action(action, False)
    # sleep(2)

    # xml = controller._get_xml()
    # parser = ETParser(xml)

    # next_button = parser.get_element(
    #     "resource-id", "com.instagram.android:id/next_button_textview"
    # )
    # next_button_bounds = parser.get_bounds(next_button)
    # next_button_x = (next_button_bounds[0] + next_button_bounds[2]) // 2
    # next_button_y = (next_button_bounds[1] + next_button_bounds[3]) // 2
    # action = {"action": "tap", "x": next_button_x, "y": next_button_y}
    # controller.exe_action(action, False)
    # sleep(2)

    # xml = controller._get_xml()
    # parser = ETParser(xml)

    # next2_button = parser.get_element("content-desc", "Next")
    # next2_button_bounds = parser.get_bounds(next2_button)
    # next2_button_x = (next2_button_bounds[0] + next2_button_bounds[2]) // 2
    # next2_button_y = (next2_button_bounds[1] + next2_button_bounds[3]) // 2
    # action = {"action": "tap", "x": next2_button_x, "y": next2_button_y}
    # controller.exe_action(action, False)
    # sleep(2)

    # xml = controller._get_xml()
    # parser = ETParser(xml)

    # share_button = parser.get_element("text", "Share")
    # share_button_bounds = parser.get_bounds(share_button)
    # share_button_x = (share_button_bounds[0] + share_button_bounds[2]) // 2
    # share_button_y = (share_button_bounds[0] + share_button_bounds[2]) // 2
    # action = {"action": "tap", "x": share_button_x, "y": share_button_y}
    # controller.exe_action(action, False)
    # sleep(2)

    # action = {"action": "home"}
    # controller.exe_action(action, False)
    # sleep(1)
