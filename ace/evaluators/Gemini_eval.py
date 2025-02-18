import base64

from ace.utils.som import draw_mark
from ace.utils.xml_cleaner import XMLCleaner
from openai import OpenAI
from pydantic import BaseModel


class GeminiEvaluator:
    def __init__(
        self, sk: str, model: str, base_url: str = "https://api.openai.com/v1"
    ) -> None:
        self.client = OpenAI(
            api_key=sk,
            base_url=base_url,
        )
        self.model = model

    def eval(
        self, task: str, xml: dict | str, screenshot: bytes, answer: str = None
    ) -> str:

        # convert screenshot to base64
        som_screenshot_base64 = base64.b64encode(screenshot).decode("utf-8")

        if answer is None:
            prompt = f"""
            Given a task, a screenshot image and a json file of the final screen, judge whether the task is completed correctly. \n
            The task is '{task}'. And here is the json file which contains elements corresponding to the marks on the screenshot: {xml}.\n
            To correctly judge the performance, you should consider element states such as 'selected' and 'activated' \\
                to check whether specific condition is satisfied. You also need to consider the content-desc attributes \\
                    of elements to check the result correctness. \n
            Answer with only "yes" or "no". The reason should consider the conflicting elements or wrong states. \n
            Use this JSON schema: \n
            {{"answer": str, "reason": str}}
            """
        else:
            prompt = f"""
            Given a task, a screenshot image and and a xml file of the final screen, judge whether the provided answer is correct for the task. \n
            The task is '{task}'. The answer of the task is: {answer}. And here is the json file which contains elements corresponding to the marks on the screenshot: {xml}. \n
            To correctly judge the performance, you should consider element states such as 'selected' and 'activated' \\
                to check whether specific condition is satisfied. You also need to consider the content-desc attributes \\
                    of elements to check the result correctness. \n
            Answer with only "yes" or "no". The reason should consider the conflicting elements or wrong states. \n
            Use this JSON schema: \n
            {{"answer": str, "reason": str}}
            """

        # Call OpenAI API
        # try:
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{som_screenshot_base64}"
                            },
                        },
                    ],
                },
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        # except Exception as e:
        #     return {
        #         "states": [],
        #         "answer": "none",
        #         "reason": f"Error in evaluating the states: {str(e)}",
        #     }

        # Extract and save generated code
        judge = response.choices[0].message.content
        judge = judge[8:-4]
        return judge


class GeminiStateEval:
    def __init__(
        self, sk: str, model: str, base_url: str = "https://api.openai.com/v1"
    ) -> None:
        self.client = OpenAI(
            api_key=sk,
            base_url=base_url,
        )
        self.model = model

    def eval_state(
        self,
        xmls: list[dict],
        screenshots: bytes,
        states: list[str],
        answer: str = None,
    ) -> str:

        states_str = "\n".join(states)

        screenshots = base64.b64encode(screenshots).decode("utf-8")

        elements = ", ".join([repr(xml) for xml in xmls])

        if answer:
            prompt = f"""
                Given a list of UI elements, an image consisting of screenshots
                and a list of states, judge whether one or more states are correctly
                achieved in the conbimed screenshots. \n
                The sequence of states is: {states_str} \n
                The sequence of UI elements corresponding to the screenshots are: {elements} \n
                You are also provided with an answer to the final question: {answer} \n
                \n
                You are required to reply with the states that are correctly achieved
                without any changes. If none of the states are correctly achieved, 
                reply with "none". \n
                If the "answer" is correct, reply with the the "answer" attribute "yes" and 
                otherwise "no". \n
                Also provide the reason for your answer. \n
                Use this JSON schema: \n
                {{"states": list[str], "answer": str, "reason": str}}
            """

        else:
            prompt = f"""
                Given a list of UI elements, an image consisting of four screenshots
                and a list of states, judge whether one or more states are correctly
                achieved in the conbimed screenshots. \n
                The list of states is: {states_str} \n
                The sequence of UI elements corresponding to the screenshots are: {elements} \n
                \n
                You are required to reply with the states that are correctly achieved
                without any changes. If none of the states are correctly achieved, 
                reply with "none". \n
                Also provide the reason for your answer. \n
                Use this JSON schema: \n
                {{"states": list[str], "reason": str}}
            """

        # Call OpenAI API
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that judge whether a task is completed correctly.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{screenshots}"
                            },
                        },
                    ],
                },
            ],
            temperature=0.7,
            max_tokens=4000,
        )

        # Extract and save generated code
        judge = response.choices[0].message.content
        judge = judge[8:-4]
        return judge
