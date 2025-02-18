import base64
from io import BytesIO

import easyocr
import numpy as np
from PIL import Image


def process_screenshot_with_bounds(
    screenshot: str,  # Base64 encoded screenshot
    bounds: tuple,  # crop bound (left, top, right, bottom)
    separator: str = " ",  # separator for combining text each line
) -> str:
    """
    get text from the specified area of the screenshot and return the combined string.

    Args:
        screenshot (str): Base64 encoded screenshot string.
        bounds (tuple): crop bound (left, top, right, bottom).
        separator (str): separator for combining text each line, default is comma " ".

    Returns:
        str: combined string of extracted text.
    """
    screenshot_data = base64.b64decode(screenshot)

    screenshot_image = Image.open(BytesIO(screenshot_data))

    cropped_image = screenshot_image.crop(bounds)

    cropped_image_np = np.array(cropped_image)
    cropped_image.save("cropped_screenshot.png")

    reader = easyocr.Reader(["en"])
    text_list = reader.readtext(cropped_image_np, detail=0)

    combined_text = separator.join(text_list)

    return combined_text


def only_screenshot_with_bounds(
    screenshot: str,  # Base64 encoded screenshot
    bounds: tuple,  # crop bound (left, top, right, bottom)
) -> bool:
    screenshot_data = base64.b64decode(screenshot)

    screenshot_image = Image.open(BytesIO(screenshot_data))

    cropped_image = screenshot_image.crop(bounds)

    cropped_image.save("cropped_screenshot.png")

    return True
