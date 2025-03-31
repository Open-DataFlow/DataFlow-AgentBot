from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx
import uuid
from Toolkits.FormatJsonTool import validate_filename, parse_jsonl, format_context
from AgentRole.Analyst import AnalystAgent
from AgentRole.TaskDispatcher import Task
import yaml
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()


class Config:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.API_KEY = config.get('API_KEY')
        self.CHAT_API_URL = config.get('CHAT_API_URL')
        self.MODEL = config.get('MODEL')
        self.local = config.get('local', False)
        self.TaskYaml = config.get('TaskYaml')
config = Config('ChatAgentYaml.yaml')
class UserMessage(BaseModel):
    content: str
class ChatAgentRequest(BaseModel):
    user_id: int
    message: UserMessage
    model: str = config.MODEL
    kb_id: str  # 改为文件标识符
class ChatInfo(BaseModel):
    id: str
    name: str
    info: str
@app.post("/chatAgent", response_model=ChatInfo)
async def chat_agent(request: ChatAgentRequest):
    try:
        if config.local:
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
                print('kb_content:'+formatted_context)
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Server error: {str(e)}"
                )
        else:
            try:
                task = Task(f'{current_dir}/TaskInfo.yaml')
                agent = AnalystAgent(task)
                formatted_context = agent.generate_analysis_report()
                print('kb_content:' + str(formatted_context))
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Server error: {str(e)}"
                )

        payload = {
            "model": request.model,
            "messages": [
                {"role": "system", "content": "Remember!! You are a Data Analysis Expert Agent!!"},
                {"role": "user",
                 "content": f"This is the overall data information of the user's knowledge base:{str(formatted_context)}\n\nUser's question：{request.message.content}"}
            ]
        }
        headers = {
            "Authorization": f"Bearer {config.API_KEY}",
            "Content-Type": "application/json"
        }
        # 发送请求到ChatAnywhere
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.CHAT_API_URL,
                json=payload,
                headers=headers,
                timeout=15.0
            )
            response.raise_for_status()

            reply = response.json()["choices"][0]["message"]["content"]

            return ChatInfo(
                id=str(uuid.uuid4()),
                name="Data Analyst Agent",
                info=reply
            )
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
