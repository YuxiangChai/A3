import re

from ace.translator.base import BaseTranslator
from openai import OpenAI


class UITarsTranslator(BaseTranslator):
    def __init__(self, sk: str = "empty") -> None:
        self.client = OpenAI(api_key="empty", base_url="http://127.0.0.1:8002/v1")
        self.prompt = r"""You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task. 

        ## Output Format
        ```\nThought: ...
        Action: ...\n```

        ## Action Space
        click(start_box='<|box_start|>(x1,y1)<|box_end|>')
        long_press(start_box='<|box_start|>(x1,y1)<|box_end|>', time='')
        type(content='') # If you want to submit your input, use \"\
        scroll(start_box='<|box_start|>(x1,y1)<|box_end|>', end_box='<|box_start|>(x3,y3)<|box_end|>')
        press_home()
        press_back()
        finished(content='') # Submit the task regardless of whether it succeeds or fails.

        ## Note
        - Use English in `Thought` part.

        - Write a small plan and finally summarize your next action (with its target element) in one sentence in `Thought` part.

        ## User Instruction
        """

    def descale_coord(self, x: int, y: int, width: int, height: int) -> tuple:
        return round(x * width / 1000), round(y * height / 1000)

    def to_device(self, action: str, width: int, height: int) -> dict:
        """transform the string generated by agent to the action that can be executed on the device

        Args:
            action (Any): any action generated by agent

        Returns:
            dict: a dictionary containing the action that can be executed on the device. The format is like:
                    {"action": "open", "app": "youtube"}
                    {"action": "tap", "x": 100, "y": 100}
                    {"action": "long_press", "x": 100, "y": 100}
                    {"action": "swipe", "x1": 100, "y1": 100, "x2": 200, "y2": 200}
                    {"action": "type", "text": "hello"}
                    {"action": "enter"}
                    {"action": "back"}
                    {"action": "home"}
                    {"action": "end", "answer": "answer to the query"}
        """
        action_str = re.search(r"Action:\s*([^\n]*)", action)
        if not action_str:
            return {"action": "end", "answer": ""}

        action_str = action_str.group(1).strip()

        if action_str.startswith("click"):
            coord_pattern = (
                r"click\(start_box='\<\|box_start\|\>\((\d+),(\d+)\)\<\|box_end\|\>'\)"
            )
            match = re.search(coord_pattern, action_str)

            if match:
                x1, y1 = int(match.group(1)), int(match.group(2))
                x1, y1 = self.descale_coord(x1, y1, width, height)
            else:
                x1, y1 = 0, 0
            return {"action": "tap", "x": x1, "y": y1}
        elif action_str.startswith("long_press"):
            coord_time_pattern = r"long_press\(start_box='\<\|box_start\|\>\((\d+),(\d+)\)\<\|box_end\|\>', time='(\d*)'\)"
            match = re.search(coord_time_pattern, action_str)

            if match:
                x1, y1, press_time = (
                    int(match.group(1)),
                    int(match.group(2)),
                    match.group(3),
                )
                x1, y1 = self.descale_coord(x1, y1, width, height)
                time = (
                    int(press_time) if press_time else 1000
                )  # Default to 1000ms if empty
            else:
                x1, y1, time = 0, 0, 1000
            return {"action": "long_press", "x": x1, "y": y1, "time": time}
        elif action_str.startswith("scroll"):
            scroll_pattern = r"scroll\(start_box='\<\|box_start\|\>\((\d+),(\d+)\)\<\|box_end\|\>', end_box='\<\|box_start\|\>\((\d+),(\d+)\)\<\|box_end\|\>'\)"
            match = re.search(scroll_pattern, action_str)

            if match:
                x1, y1 = int(match.group(1)), int(match.group(2))  # Start coordinates
                x3, y3 = int(match.group(3)), int(match.group(4))  # End coordinates

                # Scale coordinates to device dimensions
                x1, y1 = self.descale_coord(x1, y1, width, height)
                x3, y3 = self.descale_coord(x3, y3, width, height)
            else:
                x1, y1, x3, y3 = 0, 0, 0, 0
            return {"action": "swipe", "x1": x1, "y1": y1, "x2": x3, "y2": y3}
        elif action_str.startswith("type"):
            content_pattern = r"type\(content='([^']*)'\)"
            match = re.search(content_pattern, action_str)

            if match:
                text = match.group(1)  # Get the content inside quotes
            else:
                text = ""
            return {"action": "type", "text": text}
        elif action_str.startswith("press_back"):
            return {"action": "back"}
        elif action_str.startswith("press_home"):
            return {"action": "home"}
        elif action_str.startswith("wait"):
            return {"action": "wait"}
        elif action_str.startswith("finished"):
            finished_pattern = r"finished\(content='([^']*)'\)"
            match = re.search(finished_pattern, action_str)

            if match:
                content = match.group(1)
            else:
                content = ""
            return {"action": "end", "answer": content}

    def to_agent(self, state: dict, task: str, history: dict) -> str:
        """Given the current state of the device, interact with the agent and get the output

        Args:
            state (dict): a state generated by the device
                - screenshot
                - xml

        Returns:
            str: the output generated by the agent
        """

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.prompt + task,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{state['screenshot']}",
                        },
                    },
                ],
            },
        ]

        if len(history["agent_messages"]) > 0:
            messages[0]["content"].extend(
                [
                    {
                        "type": "text",
                        "text": "Your previous action is: "
                        + history["agent_messages"][-1],
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{history['screenshot'][-1]}",
                        },
                    },
                ]
            )

        response = self.client.chat.completions.create(
            messages=messages, model="UI-TARS-7B-SFT"
        )

        out_message = response.choices[0].message.content
        return out_message


def register(config: dict) -> UITarsTranslator:
    return UITarsTranslator()
