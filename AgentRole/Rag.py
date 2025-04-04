import os
import yaml
from camel.storages import QdrantStorage
from camel.retrievers import VectorRetriever
from ChatAnywhereEmbedding import ChatAnywhereEmbedding
from qdrant_client import QdrantClient
import json
from typing import List, Dict
def run_embedding_and_retrieval(config):
    # 2. 创建自定义Embedding实例
    custom_embedding = ChatAnywhereEmbedding(
        api_key=config['api_key'],
        model_name=config['model_name']
    )

    # 3. 初始化向量存储实例
    storage_instance = QdrantStorage(
        vector_dim=custom_embedding.get_output_dim(),
        path=config['path'],
        collection_name=config['collection_name'],
    )

    # 4. 初始化检索器实例
    vector_retriever = VectorRetriever(embedding_model=custom_embedding, storage=storage_instance)

    print("Processing content and indexing embeddings. This may take some time...")
    for content in config.get('contents', []):
        try:
            vector_retriever.process(content=content)
        except Exception as e:
            print(f"Error processing content {content}: {e}")
    print("Processing completed!")

    query = config['query']
    retrieved_info = vector_retriever.query(query=query, top_k=1)
    print("\nRelevant Query Result:")
    print(retrieved_info)
    
def export_collection_to_json(config):
    """
    将指定集合的文本内容合并保存为 JSON 文件

    Args:
        config: 包含配置信息的字典
    """
    # 连接数据库
    client = QdrantClient(path=config['db_path'])

    # 获取所有记录
    scroll_result = client.scroll(
        collection_name=config['collection_name'],
        limit=config['chunk_size'],
        with_payload=True,
        with_vectors=False
    )

    # 合并文本内容
    full_text = "\n".join(
        [record.payload.get("text", "") for record in scroll_result[0]]
    )

    # 构建数据结构
    output_data = {
        "collection": config['collection_name'],
        "total_records": len(scroll_result[0]),
        "original_db_path": config['db_path'],
        "content": full_text.strip()
    }
    # 保存为 JSON 文件
    with open(config['output_path']+f"{config['kb_id']}.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

def readYaml(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        return config

# 使用示例
if __name__ == "__main__":
    config = readYaml("../CamelRag.yaml")
    # export_collection_to_json(config)
    run_embedding_and_retrieval(config)