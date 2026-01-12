# A3: Android Agent Arena

_(Do not use this anymore) This is previously the official repo for Android Agent Arena (A3) [paper](https://arxiv.org/abs/2501.01149)._ **We have updated the entire benchmark including tasks, codebase and evaluation. The updated repo is named [Android Interactive Toolkit (AITK)](https://github.com/YuxiangChai/AITK)**

## Environment Setup

1. Refer to the [document](docs/environment_setup.md) to set up the Appium Server.
2. Run the following command to setup the Python environment.
   ```bash
   conda create -n ace python=3.10 -y
   conda activate ace
   pip install -r requirements.txt
   pip install -e .
   ```

**Note**: The sdk I used for Gemini is not the official Gemini sdk. I used the same OpenAI package for the Gemini model, because my APIs are from a mixed provider. The official Gemini sdk is not available and you need to modify `ace/evaluators/Gemini_eval.py` to use the official Gemini sdk. Claude is supported.

## Usage

### Task Execution

1. Modify the `config/control_config.yaml` file. (Strongly recommend to set `only_execution` to `True` so that the evaluation is not performed during the execution)
2. Run the following command to execute the task.
   ```bash
   python script/control.py
   ```

### Task Evaluation

1. Modify the `config/eval_config.yaml` file. Note: replace `sk-xxx` with your own API keys.
2. Run the following command to evaluate the task.
   ```bash
   python script/eval.py
   ```

**Note**: The default is to evaluation essential states for LLM evaluation, which may cost $15 for 201 tasks.

### Task Results

Run the following command to list the results of the evaluation.

```bash
# list the results of function evaluation
python script/print_func_results.py
# list the results of llm evaluation
python script/print_llm_results.py
```

### Customization

1. Customize tasks, please refer to [Task Customization](docs/tasks.md).
2. Customize agents, please refer to [Agent Customization](docs/agents.md).

## Under Development

- Specific app execution and evaluation
- Human annotate essential states
- Customize evaluators for LLM evaluation

## Citation

If you find this work useful, please consider citing:

```bibtex
@misc{chai2025a3androidagentarena,
      title={A3: Android Agent Arena for Mobile GUI Agents},
      author={Yuxiang Chai and Hanhao Li and Jiayu Zhang and Liang Liu and Guozhi Wang and Shuai Ren and Siyuan Huang and Hongsheng Li},
      year={2025},
      eprint={2501.01149},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2501.01149},
}
```
