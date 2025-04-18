import json
import requests
import yaml
from typing import Dict, Any
from pathlib import Path
from AgentRole.TaskDispatcher import Task
from PromptsTemplates.PromptsGenerator import PromptsTemplateGenerator


class AnalystAgent:
    def __init__(self, task: Task):
        self.task = task
        self.headers = {
            "Authorization": f"Bearer {self.task.api_key}",
            "Content-Type": "application/json"
        }

    def generate_analysis_report(self) -> Dict[str, Any]:

        # task_description = self.task.get_task_description()
        task_description = self.task.task_template
        if task_description is None:
            return {}

        json_data = {
            "model": self.task.modelname,
            "messages": [
                {"role": "system", "content": self.task.sys_prompt},
                {"role": "user", "content": task_description}
            ],
            # "response_format": {"type": "json_object"},
        }
        # print(json_data)
        response = requests.post(
            url=f"{self.task.base_url}/chat/completions",
            headers=self.headers,
            json=json_data
        )
        response.raise_for_status()
        result = response.json()
        # print(result)
        return self._parse_json(result['choices'][0]['message']['content'])


    def _parse_json(self, json_str: str) -> Dict[str, Any]:
        try:
            # 尝试直接解析
            return json.loads(json_str)
        except json.JSONDecodeError:
            # 提取首个JSON对象
            start = json_str.find('{')
            end = json_str.rfind('}') + 1
            if start != -1 and end != 0:
                cleaned_str = json_str[start:end]
                return json.loads(cleaned_str)
            else:
                raise ValueError("No valid JSON found in response")

# if __name__ == "__main__":
#     task = Task('../TaskInfo.yaml')
#     agent = AnalystAgent(task)
#     report = agent.generate_analysis_report()
#     print(report)