import json
import requests
import yaml
from typing import Dict, Any
import os
from enum import Enum
from PromptsTemplates.PromptsGenerator import PromptsTemplateGenerator

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

class TaskType(Enum):
    CONVERSATION_TASK = 0
    EXECUTION_TASK = 1

class Task:
    def __init__(self,config_path: str,prompts_template:PromptsTemplateGenerator,task_params:dict,task_goal :str = "",**kwargs):
        self.prompts_template = prompts_template
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.api_key = config['api_key']
        self.base_url = config['base_url']
        # self.json_path = f"{parent_dir}/data/knowledgebase/{config['kb_id']}.json"
        # 动态渲染所有模板
        for template_cfg in task_params.get("templates", []):
            template_name = template_cfg["name"]
            params = template_cfg.get("params", {})
            try:
                rendered = self.prompts_template.render(
                    template_name=template_name,
                    **params
                )
                if "system" in template_name.lower():
                    self.sys_prompt = rendered
                else:
                    self.task_template = rendered
            except Exception as e:
                print(f"Error rendering template {template_name}: {str(e)}")

        self.modelname = config['modelname']
        self.tasktype = TaskType(config['tasktype'])

    # def get_task_description(self):
    #     try:
    #         with open(self.json_path, 'r', encoding='utf-8') as f:
    #             kb = json.load(f)
    #         return self.task_template.format(content=kb['content'])
    #     except FileNotFoundError:
    #         print(f"Error: The JSON file {self.json_path} was not found!")
    #     except json.JSONDecodeError:
    #         print(f"Error: Unable to parse the JSON file {self.json_path}!")
    #     except Exception as e:
    #         print(f"Error: An unknown error occurred: {e}")
    #     return None

    # def get_extra_content(self):
    #     try:
    #         with open(self.json_path, 'r', encoding='utf-8') as f:
    #             kb = json.load(f)
    #         return kb['content']
    #     except FileNotFoundError:
    #         print(f"Error: The JSON file {self.json_path} was not found!")
    #     except json.JSONDecodeError:
    #         print(f"Error: Unable to parse the JSON file {self.json_path}!")
    #     except Exception as e:
    #         print(f"Error: An unknown error occurred: {e}")
    #     return None