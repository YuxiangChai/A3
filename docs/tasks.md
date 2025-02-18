# Customize Tasks

Examples are in `ace/task_eval/` folder.

You can create your own tasks for your apps as follows:

1. Create a new folder in `ace/task_eval/` with the name of your app.
2. Create a new python file in the folder with the name of your task (doesn't matter, just to be distinct in the folder).
3. Create a function named `task`, which returns a dictionary as:
   ```python
   def task() -> dict:
       return {
           "task": "your task",
           "task_level": "easy / medium/ hard",
           "category": "operation / single-page query / multi-page query",
       }
   ```
4. Create a evaluation function if you want to use the function evaluation. Leave blank if you only want to use LLM evaluation.
   ```python
   def eval(
       task: str,
       xml: str,
       screenshot: str,  # base64 string of the current screenshot
       history: dict,  # history dictionary containing xml, screenshot and action
       answer: str = None,  # agent answer
       client=None,
       model_type: str = "gpt-4o-2024-11-20",
   ) -> bool:
       pass
   ```
