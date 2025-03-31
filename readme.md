# DataFlowAgentBot
![image](images/HTq8KaoVltlotz0t7VXu4x_xgHpHOsPXdEyFwhgsAHM.png)

The DataFlowAgent is divided into two stages. In the first stage, it only functions as an intelligent chat assistant based on the user's knowledge base and does not need to complete the interactive DataFlow work.

---
### Functions in the first stage:
1. Conduct intelligent Q&A regarding the user's knowledge base, which is not limited to:
   * How to fine-tune this knowledge base using a Large Language Model (LLM)?
   * How to optimize this knowledge base?
   * What are the structure, content, domain distribution, and the proportion of structured data in the knowledge base?
2. Quick call of the AgentAPI;

```python
启动服务：
uvicorn main:app --reload

API测试：
 curl -X POST "http://localhost:8000/chatAgent" -H "Content-Type: application/json" -d '{
  "user_id": 123,
  "message": {"content": "这个知识库是干啥的？"},
  "model": "gpt-3.5-turbo",
  "kb_id": "1" #这个是用户的知识库ID，暂时没用；
}'
```
3. Q&A about the local complete knowledge base or Q&A about the knowledge base summary report;
**ChatAgentYAML：**

```python
API_KEY: sk-EeIRGDMK9OYGtsosbo9XWBg30CuW2SUltT8Zfy7Tw1Ow51Hi
CHAT_API_URL: https://api.chatanywhere.com.cn/v1/chat/completions
MODEL: gpt-4o
local: false #读入本地知识库还是获取知识库的摘要信息
TaskYaml: TaskInfo.yaml #自定义任务信息
```
**TaskInfo：**

```python
api_key: sk-EeIRGDMK9OYGtsosbo9XWBg30CuW2SUltT8Zfy7Tw1Ow51Hi
base_url: https://api.chatanywhere.com.cn/v1
modelname: gpt-4o
sys_prompt: |
  You are a professional data analyst. Please generate a structured JSON report according to the user's question. The fields are as follows:
  - summary: Summary
  - total_records: Total number of records in the data
  - domain_distribution: Dictionary of domain distribution (e.g., {"Technology": 30%, "Medical": 20%})
  - language_types: List of language types
  - data_structure: Data structuring type (e.g., {"Structured": 40%, "Unstructured": 60%})
  - has_sensitive_info: Whether it contains sensitive information
kb_id: 1
task_template: |
  Knowledge base content: {content}
  Tasks for summarizing the knowledge base:
  - Generate a detailed summary of this knowledge base as much as possible.
  - How many data records are there?
  - What is the domain distribution of the data (such as computer, technology, medical, law, etc.)?
  - What is the language type of the data (single language/multiple languages)?
  - Is the data structured (such as tables, key-value pairs) or unstructured (pure text)? What are the respective proportions?
  - Does the data contain sensitive information (such as personal privacy, business secrets)? What is the proportion?
```
4. Simple construction of Retrieval Augmented Generation (RAG);

**CamelRag：**

```python
api_key: sk-EeIRGDMK9OYGtsosbo9XWBg30CuW2SUltT8Zfy7Tw1Ow51Hi
kb_id: 2
output_path: ../data/knowledgebase/
#---------------------------------------------------------------构建RAG---------------------------------------------------------------
db_path: local_data
chunk_size: 50000
contents: ["https://www.zhihu.com/question/652674711/answer/3617998488",'https://mmssai.com/archives/30317']
collection_name: LearnRAG 
query: 什么是RAG？？
model_name: text-embedding-ada-002 #指定Embedding模型
path: local_data
```
Based on the content of the links (it can also be based on PDFs, TXTs, etc.) \["[https://www.zhihu.com/question/652674711/answer/3617998488](https://www.zhihu.com/question/652674711/answer/3617998488)", "[https://mmssai.com/archives/30317](https://mmssai.com/archives/30317)"\], construct:

```python
python AgentRole/Rag.py 
```
5. Customization of Agent tasks;
6. ......

---
### Functions in the second stage:
1. Combine with the full-link DataFlow Pipeline to achieve interactive data processing;
2. ......

---














