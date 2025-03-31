from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx
import json
import uuid
import os
from typing import List, Dict
from pathlib import Path

MAX_JSONL_LINES = 50
DATA_DIR = Path("./data/knowledgebase")  # 本地数据存储目录
def validate_filename(kb_id: str) -> Path:
    """验证并生成安全文件路径"""
    if not kb_id.endswith(".jsonl"):
        kb_id += ".jsonl"

    # 防止路径遍历攻击
    if '/' in kb_id or '\\' in kb_id:
        raise ValueError("Invalid file name")

    file_path = DATA_DIR / kb_id
    if not file_path.exists():
        raise FileNotFoundError(f"File {kb_id} not found")

    return file_path


def parse_jsonl(file_path: Path) -> List[Dict]:
    """从本地文件解析JSONL数据"""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:MAX_JSONL_LINES]
    except Exception as e:
        raise IOError(f"File read error: {str(e)}")

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                raise ValueError(f"Line {idx} is not a JSON object")
            results.append(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON at line {idx}: {str(e)}")

    return results


def format_context(data: List[Dict]) -> str:
    """将JSON数据格式化为自然语言上下文"""
    context = ["以下是知识库中的结构化数据："]

    for item in data:
        context.append("条目包含以下字段：")
        for key, value in item.items():
            context.append(f"- {key}: {str(value)[:200]}")  # 限制单个字段长度

    return "\n".join(context)