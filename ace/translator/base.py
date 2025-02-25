class BaseTranslator:
    def __init__(self) -> None:
        pass

    def to_device(self, action: str) -> dict:
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
                    {"action": "end"}
        """
        return {}

    def to_agent(self, state: dict) -> str:
        """Given the current state of the device, interact with the agent and get the output

        Args:
            state (dict): a state generated by the device

        Returns:
            str: the output generated by the agent
        """
        return "CLICK[100,100]"
