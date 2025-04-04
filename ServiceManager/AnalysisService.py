from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx
import uuid
from Toolkits.Tools import validate_filename, parse_jsonl, format_context,get_kb_content,ChatResponse,ChatAgentRequest

from AgentRole.Analyst import AnalystAgent
from AgentRole.TaskDispatcher import Task
import yaml
import os
from PromptsTemplates.PromptsGenerator import PromptsTemplateGenerator
current_dir = os.path.dirname(os.path.abspath(__file__))


class Config:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.API_KEY = config.get('API_KEY')
        self.CHAT_API_URL = config.get('CHAT_API_URL')
        self.MODEL = config.get('MODEL')
        self.LOCAL = config.get('local', False)
        self.TaskYaml = config.get('TaskYaml')
        self.HEADER = {
                "Authorization": f"Bearer {self.API_KEY}",
                "Content-Type": "application/json"
            }

class AnalysisService:
    def __init__(self, config_path: str,task:Task):
        self.config = Config(config_path)
        self.task =  task

    def _build_payload(self, request, context):
        return {
            "model": request.model,
            "messages": [
                {"role": "system", "content": "Data Analysis Expert"},
                {"role": "user", "content": f"Context: {context}\nQuestion: {request.message}\n.(Answer in {self.task.prompts_template.output_language}!!!);"}
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }
    async def _call_llm_api(self, request, context):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config.CHAT_API_URL,
                json=self._build_payload(request, context),
                headers=self.config.HEADER,
                timeout=15.0
            )
            response.raise_for_status()
            return self._format_response(response)

    def _format_response(self, response):
        return ChatResponse(
            id=str(uuid.uuid4()),
            name="Analysis Agent",
            info=response.json()["choices"][0]["message"]["content"]
        )

    async def process_request(self, request: ChatAgentRequest):
        try:
            if self.config.LOCAL:
                try:
                    # 验证并获取文件路径
                    try:
                        file_path = validate_filename(request.kb_id)
                    except (ValueError, FileNotFoundError) as e:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e)
                        )
                    # 从本地文件解析数据
                    try:
                        json_data = parse_jsonl(file_path)
                    except (IOError, ValueError) as e:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"File processing error: {str(e)}"
                        )
                    formatted_context = format_context(json_data)
                    print('kb_content:' + formatted_context)
                except HTTPException as e:
                    raise e
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Server error: {str(e)}"
                    )
            else:
                try:
                    agent = AnalystAgent(self.task)
                    formatted_context = agent.generate_analysis_report()
                    print('kb_content:' + str(formatted_context))
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Server error: {str(e)}"
                    )
            # 发送请求到ChatAnywhere
            return await self._call_llm_api(request,str(formatted_context))

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"API failed: {e.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Server error: {str(e)}"
            )

    def generate_pre_task_config(self,system_template:str,task_template:str,request:ChatAgentRequest):
        return {
            "templates": [
                {
                    "name": system_template,
                    "params": {}  # 不需要额外参数
                },
                {
                    "name": task_template,
                    "params": {
                        "content": get_kb_content(request.kb_id)
                    }
                }
            ]
        }