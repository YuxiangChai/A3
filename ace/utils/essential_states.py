from openai import OpenAI
from pydantic import BaseModel


class State(BaseModel):
    state: str


class Response(BaseModel):
    answer: list[State]


class GPTStateGen:
    def __init__(
        self, sk: str, model: str, base_url: str = "https://api.openai.com/v1"
    ) -> None:
        self.client = OpenAI(
            api_key=sk,
            base_url=base_url,
        )
        self.model = model

    def generate_states(self, task: str) -> str:

        prompt = f"""
            You are given a task instruction, which a user wants to perform on a mobile device.\n
            The task is: {task}\n
            The task can be splited by a sequence of essential states, which means the states that are necessary to achieve the task.\n
            For example, if the task is "Open Booking.com and search for one-way flight from Beijing to Shanghai on Feb 20. Select two adults." 
                the essential states are: ["Device is in Booking.com app", "One-way flight is selected", "Departure city is set to Beijing", "Arrival city is set to Shanghai", "Departure date is set to Feb 20",  "Number of adults is set to 2", "Search results are displayed"]\n
            Now please provide the essential states to achieve the task. Do not include trivial states like "Device is in Home page" or "Device is unlocked". Only include the states that are necessary to achieve the task.\n
        """

        # Call OpenAI API
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
                    ],
                },
            ],
            temperature=0.7,
            response_format=Response,
        )

        # Extract and save generated code
        states = response.choices[0].message.content
        return states
