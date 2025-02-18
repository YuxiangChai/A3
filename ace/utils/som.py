import base64
import random

import cv2
import numpy as np


def get_colors(num):
    colors = []
    dx = 1.0 / (num + 1)
    for i in range(num):
        colors.append(get_color(i * dx))
    return colors


def get_color(x):
    r, g, b = 0.0, 0.0, 1.0
    if 0.0 <= x < 0.2:
        x = x / 0.2
        r, g, b = 0.0, x, 1.0
    elif 0.2 <= x < 0.4:
        x = (x - 0.2) / 0.2
        r, g, b = 0.0, 1.0, 1.0 - x
    elif 0.4 <= x < 0.6:
        x = (x - 0.4) / 0.2
        r, g, b = x, 1.0, 0.0
    elif 0.6 <= x < 0.8:
        x = (x - 0.6) / 0.2
        r, g, b = 1.0, 1.0 - x, 0.0
    elif 0.8 <= x <= 1.0:
        x = (x - 0.8) / 0.2
        r, g, b = 1.0, 0.0, x
    return (int(r * 255), int(g * 255), int(b * 255))


def draw_mark(image: str, elements: list[dict]) -> bytes:
    """Draw marks on the image

    Args:
        image (str): The base64 string of the image
        elements (list): The elements to be marked

    Returns:
        bytes: The bytes of the marked image
    """
    # Decode base64 to numpy array
    img_bytes = base64.b64decode(image)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    ss = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Draw marks
    colors = get_colors(len(elements))
    random.shuffle(colors)

    for i, ele in enumerate(elements):
        x1, y1, x2, y2 = ele["bounds"] if "bounds" in ele else ele["bbox"]
        ss = cv2.rectangle(ss, (x1, y1), (x2, y2), colors[i], 5)
        (w, h), _ = cv2.getTextSize(str(i + 1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
        ss = cv2.rectangle(ss, (x1, y1), (x1 + w, y1 + 50), (121, 215, 190), -1)
        ss = cv2.putText(
            ss,
            str(i + 1),
            (x1, y1 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 0),
            3,
        )

    # convert numpy array to bytes
    _, buffer = cv2.imencode(".png", ss)
    img_bytes = buffer.tobytes()
    return img_bytes
