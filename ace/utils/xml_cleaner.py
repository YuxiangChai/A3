import xml.etree.ElementTree as ET
from pathlib import Path


class XMLCleaner:
    def __init__(self, xml) -> None:
        if isinstance(xml, str):
            self.et = ET.ElementTree(ET.fromstring(xml))
        elif isinstance(xml, Path):
            self.et = ET.parse(xml)
        self.w = int(self.et.getroot().attrib["width"])
        self.h = int(self.et.getroot().attrib["height"])

    def _filter_elements(self) -> list[ET.Element]:
        """return a list of elements that have the specified attributes

        Returns:
            list[ET.Element]: a list of elements that have the specified attributes
        """

        elements = []

        for ele in self.et.iter():
            if "bounds" in ele.attrib:
                if "content-desc" in ele.attrib and ele.attrib["content-desc"] != "":
                    elements.append(ele)
                elif "text" in ele.attrib and ele.attrib["text"] != "":
                    elements.append(ele)
                elif "clickable" in ele.attrib and ele.attrib["clickable"] == "true":
                    elements.append(ele)
        return elements

    def _parse_bounds(self, bounds: str) -> tuple[int, int, int, int]:
        """parse the bounds string to x1, y1, x2, y2

        Args:
            bounds (str): the bounds string

        Returns:
            tuple[int, int, int, int]: x1, y1, x2, y2
        """
        x1, y1 = bounds.split("][")[0].replace("[", "").split(",")
        x2, y2 = bounds.split("][")[1].replace("]", "").split(",")
        return int(x1), int(y1), int(x2), int(y2)

    def _calculate_iou(self, box1, box2) -> float:
        """Calculate IoU between two boxes"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2

        # Calculate intersection
        x1_i = max(x1_1, x1_2)
        y1_i = max(y1_1, y1_2)
        x2_i = min(x2_1, x2_2)
        y2_i = min(y2_1, y2_2)

        if x2_i <= x1_i or y2_i <= y1_i:
            return 0.0

        intersection = (x2_i - x1_i) * (y2_i - y1_i)

        # Calculate union
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union = area1 + area2 - intersection

        return intersection / union

    def _rm_overlap_elements(
        self, elements: list, iou_threshold: float = 0.9
    ) -> list[ET.Element]:
        """Remove overlapped elements using NMS with IoU threshold

        Args:
            elements (list): List of elements
            iou_threshold (float): IoU threshold for NMS
        """
        if not elements:
            return []

        # Sort by y1 coordinate
        elements = sorted(
            elements, key=lambda x: self._parse_bounds(x.attrib["bounds"])[1]
        )

        # NMS
        kept_elements = []
        while len(elements) > 0:
            current = elements[0]
            kept_elements.append(current)

            current_bounds = self._parse_bounds(current.attrib["bounds"])
            elements = elements[1:]

            filtered_elements = []
            for element in elements:
                element_bounds = self._parse_bounds(element.attrib["bounds"])
                iou = self._calculate_iou(current_bounds, element_bounds)

                if iou < iou_threshold:
                    filtered_elements.append(element)

            elements = filtered_elements

        return kept_elements

    def _rm_bigger_cover_elements(self, elements: list) -> list[ET.Element]:
        """Remove elements that completely surround smaller elements

        Args:
            elements (list): List of elements with bounds attributes

        Returns:
            list[ET.Element]: Filtered elements with containers removed
        """
        if not elements:
            return []

        def get_area(element):
            x1, y1, x2, y2 = self._parse_bounds(element.attrib["bounds"])
            return (x2 - x1) * (y2 - y1)

        def is_contained(box1, box2):
            """Check if box1 is contained within box2"""
            x1_1, y1_1, x2_1, y2_1 = box1
            x1_2, y1_2, x2_2, y2_2 = box2
            return x1_2 <= x1_1 and y1_2 <= y1_1 and x2_2 >= x2_1 and y2_2 >= y2_1

        # Sort by area ascending
        elements = sorted(elements, key=get_area)

        kept_elements = []
        for i, elem in enumerate(elements):
            current_bounds = self._parse_bounds(elem.attrib["bounds"])
            is_container = False

            # Check if this element contains any smaller elements
            for smaller_elem in elements[:i]:
                smaller_bounds = self._parse_bounds(smaller_elem.attrib["bounds"])
                if is_contained(smaller_bounds, current_bounds):
                    is_container = True
                    break

            if not is_container:
                kept_elements.append(elem)

        return kept_elements

    def get_final_elements(self) -> list[dict]:
        """Get the final elements after filtering and NMS

        Returns:
            list[dict]: The final elements
        """
        elements = self._filter_elements()
        elements = self._rm_overlap_elements(elements)
        elements = self._rm_bigger_cover_elements(elements)

        elements = sorted(
            elements, key=lambda x: self._parse_bounds(x.attrib["bounds"])[1]
        )

        ret = []

        for ele in elements:
            bounds = self._parse_bounds(ele.attrib["bounds"])
            content_desc = ele.attrib.get("content-desc", "")
            text = ele.attrib.get("text", "")
            clickable = ele.attrib.get("clickable", "")
            ret.append(
                {
                    "bounds": bounds,
                    "content-desc": content_desc,
                    "text": text,
                    "clickable": clickable,
                }
            )

        return ret
