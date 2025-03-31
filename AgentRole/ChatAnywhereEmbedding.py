import os
import httpx
from typing import Any, List
from camel.embeddings import BaseEmbedding


class ChatAnywhereEmbedding(BaseEmbedding[str]):
    """Custom embedding model using ChatAnywhere API"""

    def __init__(self, api_key: str, model_name: str = "text-embedding-ada-002"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = "https://api.chatanywhere.tech/v1/embeddings"
        self._output_dim = 1536  # 根据实际模型维度调整

    def embed_list(self, objs: List[str], **kwargs: Any) -> List[List[float]]:
        """获取批量文本的嵌入向量"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "input": objs,
            "model": self.model_name
        }

        try:
            with httpx.Client() as client:
                response = client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()

                embeddings = []
                for item in response.json()["data"]:
                    embeddings.append(item["embedding"])
                return embeddings

        except Exception as e:
            raise RuntimeError(f"Embedding request failed: {str(e)}")

    def get_output_dim(self) -> int:
        return self._output_dim