# Customize Agents

Examples are in `ace/translator/` folder.

You can create your own agents as follows:

1. Create a new python file in the `ace/translator/` folder with the name of your agent.
2. Create a class inheriting from `BaseAgent`, which should contain the following methods:
   - `to_agent`, which takes inputs `state`, `task` and `history`. It should use the input information and interact with the agent to predict the agent's response.
   - `to_device`, which takes inputs `action` (agent's response), `width` and `height`. It should convert the agent's response message to the standard A3 action format.
3. Create a function which returns the agent object as:
   ```python
   def agent() -> BaseAgent:
       return YourAgent()
   ```
4. Modify the agent name in `config/control_config.yaml` to use your agent. You should put the exact name of the agent file in the `agent` field.

Check the `ace/translator/ui_tars.py` for detailed implementation.
