from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx
import uuid
from Toolkits.Tools import get_kb_content,ChatResponse,ChatAgentRequest,generate_pre_task_params
from AgentRole.TaskDispatcher import Task
import yaml
import os
from PromptsTemplates.PromptsGenerator import PromptsTemplateGenerator
from ServiceManager.AnalysisService import AnalysisService
current_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
# 在路由处理中动态创建配置

@app.post("/chatAgent", response_model=ChatResponse)
async def chat_agent(request:ChatAgentRequest):
    prompts_template = PromptsTemplateGenerator(f"{request.language}")
    # prompts_template.add_sys_template()
    # prompts_template.add_task_template()
    # 必须执行的任务
    task_for_analysis = Task(config_path=f'{current_dir}/TaskInfo.yaml',
                                  prompts_template=prompts_template,
                                  task_params=generate_pre_task_params("system_prompt_for_KBSummary",
                                                                       "task_summarize_template", request))
    task_for_recommand =  Task(config_path=f'{current_dir}/TaskInfo.yaml',
                                  prompts_template=prompts_template,
                                  task_params=generate_pre_task_params("system_prompt_for_KBSummary",
                                                                       "task_summarize_template", request))
    TaskList = [task_for_analysis,task_for_recommand]
    analysisService = AnalysisService('ChatAgentYaml.yaml',task_for_analysis)
    return await analysisService.process_request(request=request)