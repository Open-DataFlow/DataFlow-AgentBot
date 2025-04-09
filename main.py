from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx
import uuid
from Toolkits.Tools import get_kb_content, ChatResponse, ChatAgentRequest, generate_pre_task_params
from AgentRole.TaskDispatcher import Task
import yaml
import os
from PromptsTemplates.PromptsGenerator import PromptsTemplateGenerator
from ServiceManager.AnalysisService import AnalysisService

current_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
@app.post("/analyze", response_model=ChatResponse)
async def analysis_task(request: ChatAgentRequest):
    """知识库问答分析专用端点"""
    # 创建分析任务专属配置
    prompts_template = PromptsTemplateGenerator(f"{request.language}")

    analysis_task = Task(
        config_path=f'{current_dir}/TaskInfo.yaml',
        prompts_template=prompts_template,
        task_params=generate_pre_task_params(
            system_template="system_prompt_for_KBSummary",
            task_template="task_prompt_for_summarize",
            request=request
        )
    )

    analysis_service = AnalysisService('ChatAgentYaml.yaml', analysis_task)
    return await analysis_service.process_request(request=request)


@app.post("/recommend", response_model=ChatResponse)
async def recommendation_task(request: ChatAgentRequest):
    """Pipeline推荐专用端点"""
    # 创建推荐任务专属配置
    prompts_template = PromptsTemplateGenerator(f"{request.language}")

    recommendation_task = Task(
        config_path=f'{current_dir}/TaskInfo.yaml',
        prompts_template=prompts_template,
        task_params=generate_pre_task_params(
            system_template="system_prompt_for_recommendation_inference_pipeline",
            task_template="task_prompt_for_recommendation_inference_pipeline",
            request=request
        )
    )

    recommendation_service = AnalysisService('ChatAgentYaml.yaml', recommendation_task)
    return await recommendation_service.process_request(request=request)