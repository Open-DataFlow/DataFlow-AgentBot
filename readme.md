# DataFlowAgentBot
![image](images/HTq8KaoVltlotz0t7VXu4x_xgHpHOsPXdEyFwhgsAHM.png)

The DataFlowAgent is divided into two stages. In the first stage, it only functions as an intelligent chat assistant based on the user's knowledge base and does not need to complete the interactive DataFlow work.

---

**2025-4-5：**

- Optimize the code structure;
- Improve the creation process of task workflows;
- Utilize `PromptsTemplateGenerator` to initialize and add new task templates as well as system templates;
- Enable setting language requirements for responses;

**Pending Updates:**

1. Pipeline recommendations;
2. **`PromptsTemplate`** self-synthesis

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
  "message": {"content": "对于这样的一个知识库，我们可以微调么？要如何去微调？？用什么模型？"},
  "model": "gpt-3.5-turbo",
  "kb_id": "1",
  "max_tokens":"4000",
  "temperature": "1.0",
  "language":"Chinese"                                 
}'

```
3. Q&A about the local complete knowledge base or Q&A about the knowledge base summary report;
**ChatAgentYAML：**

```python
API_KEY: sk-ao5wGhCOAWidgaEK3WEcqWbk5a1KP8SSMsnOAy9IeRQNylVs
CHAT_API_URL: https://api.chatanywhere.com.cn/v1/chat/completions
MODEL: gpt-3.5-turbo
local: false #读入本地知识库还是获取知识库的摘要信息
TaskYaml: TaskInfo.yaml
```
**TaskInfo：**

```python
api_key: sk-ao5wGhCOAWidgaEK3WEcqWbk5a1KP8SSMsnOAy9IeRQNylVs
base_url: https://api.chatanywhere.com.cn/v1
modelname: gpt-3.5-turbo
tasktype: 0
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











