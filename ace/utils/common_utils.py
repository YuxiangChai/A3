import logging
from pathlib import Path

import cv2
import numpy as np
from ace.utils.xml_cleaner import XMLCleaner
from openai import OpenAI


def check_create_dir(path: Path) -> Path:
    if not path.is_dir():
        path.mkdir(parents=True)
    return path


def get_logger(log_dir: Path = None, name: str = "AVD-control") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_dir:
        fh = logging.FileHandler(log_dir / f"{name}.log", mode="a")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def print_results(results: dict) -> None:
    yes_3 = 0
    yes_2 = {
        "gpt": 0,
        "gemini": 0,
        "claude": 0,
    }
    yes_1 = {
        "gpt": 0,
        "gemini": 0,
        "claude": 0,
    }
    yes_0 = 0
    success = 0
    fail = 0
    not_count = 0
    for result in results:
        task = result["task"]
        task_idx = result["task_idx"]
        res = result["result"]

        if res["gpt"] == 1 and res["gemini"] == 1 and res["claude"] == 1:
            yes_3 += 1
            success += 1
        elif res["gpt"] == 1 and res["gemini"] == 1 and res["claude"] != 1:
            yes_2["gpt"] += 1
            yes_2["gemini"] += 1
            success += 1
        elif res["gpt"] == 1 and res["gemini"] != 1 and res["claude"] == 1:
            yes_2["gpt"] += 1
            yes_2["claude"] += 1
            success += 1
        elif res["gpt"] != 1 and res["gemini"] == 1 and res["claude"] == 1:
            yes_2["gemini"] += 1
            yes_2["claude"] += 1
            success += 1
        elif res["gpt"] == 1 and res["gemini"] == 0 and res["claude"] == 0:
            yes_1["gpt"] += 1
            fail += 1
        elif res["gpt"] == 0 and res["gemini"] == 1 and res["claude"] == 0:
            yes_1["gemini"] += 1
            fail += 1
        elif res["gpt"] == 0 and res["gemini"] == 0 and res["claude"] == 1:
            yes_1["claude"] += 1
            fail += 1
        elif res["gpt"] == 0 and res["gemini"] == 0 and res["claude"] == 0:
            yes_0 += 1
            fail += 1
        else:
            not_count += 1

    print(f"Success: {success}")
    print(f"Fail: {fail}")
    print(f"Success Rate: {success / (success + fail):.2f}")


def compress_image(image_bytes: bytes, max_size_mb: float = 5.0) -> bytes:
    """Compress image to be under specified size in MB while maintaining aspect ratio"""

    # Convert bytes to cv2 image
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Initial quality and scale
    quality = 95
    scale = 1.0

    while True:
        # Encode image with current parameters
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, encoded_img = cv2.imencode(".png", img, encode_param)

        # Check size
        size_mb = len(encoded_img.tobytes()) / (1024 * 1024)

        if size_mb <= max_size_mb:
            return encoded_img.tobytes()

        # Reduce quality first
        if quality > 80:
            quality -= 5
        # Then start scaling down if quality reduction isn't enough
        else:
            scale *= 0.9
            width = int(img.shape[1] * scale)
            height = int(img.shape[0] * scale)
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
            quality = 95  # Reset quality for the smaller image


def combine_screenshots(screenshots: list[bytes], max_size_mb: float = 5.0) -> bytes:
    images = [
        cv2.imdecode(np.frombuffer(s, np.uint8), cv2.IMREAD_COLOR) for s in screenshots
    ]
    middle = np.zeros((images[0].shape[0], 50, 3), np.uint8)

    # Insert middle bar between images
    combined_list = []
    for i, img in enumerate(images):
        combined_list.append(img)
        if i < len(images) - 1:
            combined_list.append(middle)
    combined = np.hstack(combined_list)
    combined = cv2.imencode(".png", combined)[1].tobytes()
    return combined


def parse_xmls(xmls: list[str]) -> list[dict]:
    ret = []
    for xml in xmls:
        elements = XMLCleaner(xml).get_final_elements()
        ret.append(elements)
    return ret


def answer_correct_judge(
    question: str,
    answer: str,
    gt: str,
    api_key: str,
    model: str = "gpt-4o-gpt-4o-2024-11-20",
) -> bool:
    client = OpenAI(
        api_key=api_key,
        base_url="https://aihubmix.com/v1",
    )

    prompt = f"You need to judge whether the answer is correct or not based on \
        the ground truth answer. The question is '{question}'. The ground truth \
        answer is '{gt}'. You need to judge whether the answer '{answer}' is correct or not. \
        If the answer is correct, please select 'Yes'. If the answer is incorrect, please select 'No'."

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=1.0,
        max_tokens=1000,
    )

    judge = response.choices[0].message.content
    if judge == "Yes":
        return True
    else:
        return False
