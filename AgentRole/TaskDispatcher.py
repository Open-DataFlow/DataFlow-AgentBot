import json
import requests
import yaml
from typing import Dict, Any
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

class Task:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.api_key = config['api_key']
        self.base_url = config['base_url']
        self.sys_prompt = config['sys_prompt']
        self.json_path = f"{parent_dir}/data/knowledgebase/{config['kb_id']}.json"
        self.task_template = config['task_template']
        self.modelname = config['modelname']

    def get_task_description(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            return self.task_template.format(content=kb['content'])
        except FileNotFoundError:
            print(f"Error: The JSON file {self.json_path} was not found!")
        except json.JSONDecodeError:
            print(f"Error: Unable to parse the JSON file {self.json_path}!")
        except Exception as e:
            print(f"Error: An unknown error occurred: {e}")
        return None
