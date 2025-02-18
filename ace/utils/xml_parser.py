import xml.etree.ElementTree as ET
from pathlib import Path


class ETParserLite:
    def __init__(self, xml: str | Path) -> None:
        if isinstance(xml, str):
            self.et = ET.ElementTree(ET.fromstring(xml))
        elif isinstance(xml, Path):
            self.et = ET.parse(xml)
        self.w = int(self.et.getroot().attrib["width"])
        self.h = int(self.et.getroot().attrib["height"])

    def get_element_by_attr_value(self, attr: str, value: str) -> ET.Element:
        for el in self.et.iter():
            if attr in el.attrib and el.attrib[attr].lower() == value.lower():
                return el

    def get_element_by_attr_value_contains(self, attr: str, value: str) -> ET.Element:
        for el in self.et.iter():
            if attr in el.attrib and el.attrib[attr].lower().find(value.lower()) != -1:
                return el

    def get_element_by_conditions(self, conditions: dict) -> ET.Element:
        for el in self.et.iter():
            # Check if all conditions are met
            if all(
                el.attrib.get(attr).lower() == value.lower()
                for attr, value in conditions.items()
            ):
                return el
        return None  # Return None if no element matches

    def find_parent(self, child_element: ET.Element) -> ET.Element:
        return child_element.find("..")

    def get_bounds(element: ET.Element) -> list[int]:
        # "[1,2][3,4]" -> [1,2,3,4]
        bounds_str = element.attrib["bounds"].replace("][", ",")
        bounds_str = bounds_str.strip("[]")
        bounds = list(map(int, bounds_str.split(",")))

        return bounds


class ETParser:
    def __init__(self, xml) -> None:
        if isinstance(xml, str):
            self.et = ET.ElementTree(ET.fromstring(xml))
        elif isinstance(xml, Path):
            self.et = ET.parse(xml)
        self.w = int(self.et.getroot().attrib["width"])
        self.h = int(self.et.getroot().attrib["height"])

    def get_element(self, attr: str, name: str) -> ET.Element:
        for el in self.et.iter():
            if attr in el.attrib and el.attrib[attr].lower() == name.lower():
                return el

    def get_elements(self, xpath: str) -> list:
        """
        获取所有符合给定 XPath 的元素
        """
        # 使用 XPath 表达式找到符合条件的所有元素
        return self.et.findall(xpath)

    def get_element_contains(self, attr: str, name: str) -> ET.Element:
        for el in self.et.iter():
            if attr in el.attrib:
                if el.attrib[attr].lower().find(name.lower()) != -1:
                    return el

    def get_element_contains_from_contains(
        self, attr: str, name: str, u_attr: str, u_name: str, position: int = -1
    ) -> ET.Element:
        """
        Find the first element that contains info provided in `attr` and `name` field begin with u_attr contains u_name.

        Args:
            attr (str): Element's attribute
            name (str): Element's attribute's value
            u_attr (str): Upper limit's attribute
            u_name (str): Upper limit's attribute's value
            position (int): Confine the appearence position to the desired position. eg. We only want first position to be 5.

        Returns:
            ET.Element: Desired element
        """
        flag = False
        for el in self.et.iter():
            if (
                u_attr in el.attrib
                and el.attrib[u_attr].lower().find(u_name.lower()) != -1
                and not flag
            ):
                flag = True
                continue
            if flag:
                if position == -1:
                    if (
                        attr in el.attrib
                        and el.attrib[attr].lower().find(name.lower()) != -1
                    ):
                        return el
                else:
                    if (
                        attr in el.attrib
                        and el.attrib[attr].lower().find(name.lower()) == position
                    ):
                        return el
        # return None if nothing was found
        return None

    def get_element_contains_from_until(
        self,
        attr: str,
        name: str,
        u_attr: str,
        u_name: str,
        l_attr: str = None,
        l_name: str = None,
        position: int = -1,
    ) -> ET.Element:
        """
        Find the first element that contains info provided in `attr` and `name` field within range.

        Args:
            attr (str): Element's attribute
            name (str): Element's attribute's value
            u_attr (str): Upper limit's attribute
            u_name (str): Upper limit's attribute's value
            l_attr (str): Lower limit's attribute
            l_name (str): Lower limit's attribute's value
            position (int): Confine the appearence position to the desired position. eg. We only want first position to be 5.

        Returns:
            ET.Element: Desired element
        """
        flag = False
        for el in self.et.iter():
            if (
                u_attr in el.attrib
                and el.attrib[u_attr].lower() == u_name.lower()
                and not flag
            ):
                flag = True
            if flag:
                # meet lower limit, end finding
                if l_attr in el.attrib and el.attrib[l_attr].lower() == l_name.lower():
                    break
                if position == -1:
                    if (
                        attr in el.attrib
                        and el.attrib[attr].lower().find(name.lower()) != -1
                    ):
                        return el
                else:
                    if (
                        attr in el.attrib
                        and el.attrib[attr].lower().find(name.lower()) == position
                    ):
                        return el
        # return None if nothing was found
        return None

    def get_element_contains_from(
        self, attr: str, name: str, u_attr: str, u_name: str, position: int = -1
    ) -> ET.Element:
        """
        Find the first element that contains info provided in `attr` and `name` field within range.

        Args:
            attr (str): Element's attribute
            name (str): Element's attribute's value
            u_attr (str): Upper limit's attribute
            u_name (str): Upper limit's attribute's value
            position (int): Confine the appearence position to the desired position. eg. We only want first position to be 5.

        Returns:
            ET.Element: Desired element
        """
        flag = False
        for el in self.et.iter():
            if (
                u_attr in el.attrib
                and el.attrib[u_attr].lower() == u_name.lower()
                and not flag
            ):
                flag = True
                continue
            if flag:
                if position == -1:
                    if (
                        attr in el.attrib
                        and el.attrib[attr].lower().find(name.lower()) != -1
                    ):
                        return el
                else:
                    if (
                        attr in el.attrib
                        and el.attrib[attr].lower().find(name.lower()) == position
                    ):
                        return el
        # return None if nothing was found
        return None

    def get_element_bydic(self, conditions: dict) -> ET.Element:
        """
        Find the first element that matches all conditions provided in the `conditions` dictionary.
        :param conditions: A dictionary where keys are attribute names and values are the expected values.
        :return: The matching element or None if not found.
        """
        for el in self.et.iter():
            # Check if all conditions are met
            if all(
                attr in el.attrib and el.attrib[attr].lower() == value.lower()
                for attr, value in conditions.items()
            ):
                return el
        return None  # Return None if no element matches

    def find_parent(self, child_element: ET.Element) -> ET.Element:
        """
        手动遍历树找到父元素，因为 ElementTree 不支持 getparent()
        """
        for parent in self.et.iter():
            if child_element in parent:
                return parent
        return None

    def find_clickable_parent(self, child_element: ET.Element) -> ET.Element:
        """
        手动遍历树找到可以点击的父元素，因为 ElementTree 不支持 getparent()
        """
        if "clickable" in child_element.attrib:
            if child_element.attrib["clickable"] == "true":
                return child_element
        else:
            return None
        for parent in self.et.iter():
            if child_element in parent:
                # if parent.attrib["clickable"] == "true":
                #     return parent
                # else:
                return self.find_clickable_parent(parent)
        # return None

    def get_bounds(self, element: ET.Element) -> list[int]:
        """Get the bounds of the element

        Args:
            element (ET.Element):

        Returns:
            list[int]: [x1, y1, x2, y2]
        """

        # "[1,2][3,4]" -> [1,2,3,4]
        bounds_str = element.attrib["bounds"].replace("][", ",")

        # 1. 去掉方括号
        bounds_str = bounds_str.strip("[]")

        # 2. 将字符串按逗号分割
        bounds = list(map(int, bounds_str.split(",")))

        return bounds
