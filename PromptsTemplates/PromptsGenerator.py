class PromptsTemplateGenerator:
    def __init__(self,output_language:str):
        self.output_language = output_language
        self.templates = {
            'system_prompts': (
                "You are a professional data analyst. "
            ),
            'task_prompt_for_summarize': (
                "Knowledge base content: {content}\n"
                "Tasks for summarizing the knowledge base:\n"
                "- Generate a detailed summary of this knowledge base as much as possible.\n"
                "- How many data records are there?\n"
                "- What is the domain distribution of the data (such as computer, technology, medical, law, etc.)?\n"
                "- What is the language type of the data (single language/multiple languages)?\n"
                "- Is the data structured (such as tables, key-value pairs) or unstructured (pure text)? What are the respective proportions?\n"
                "- Does the data contain sensitive information (such as personal privacy, business secrets)? What is the proportion?\n"
                "- Could you provide the topic coherence score of the knowledge base content, the relationships and their intensities between different concepts or entities, and the sentiment distribution?"
            ),
            'system_prompt_for_KBSummary': (
                "You are a professional data analyst. Please generate a structured JSON report according to the user's question. "
                "The fields are as follows:\n"
                "  - summary: Comprehensive analysis summary\n"
                "  - total_records: Total number of records (with growth trend analysis)\n"
                "  - domain_distribution: Dictionary of domain distribution (e.g., {{\"Technology\": 0.3, \"Medical\": 0.2}})\n"  # 修复这里
                "  - language_types: List of language types with proportions\n"
                "  - data_structure: Data structuring type (e.g., {{\"Structured\": 40%, \"Unstructured\": 60%}})\n"  # 修复这里
                "  - has_sensitive_info: Whether contains sensitive information with risk level\n"
                "  - content_analysis: {{\n"  # 修复这里
                "      \"key_topics\": [\"topic1\", \"topic2\"],\n"
                "      \"entity_linkage\": {{\"Python->AI\": 15, \"Java->Enterprise\": 20}},\n"  # 修复这里
                "      \"semantic_density\": \"high/medium/low\"\n"
                "    }}\n"  # 修复这里
            ),
            'system_prompt_for_recommendation_inference_pipeline': (
                "You are a data processing expert. Please generate a structured JSON report according to the user's question.\n"
                "Based on the user's knowledge base data, you will recommend a suitable data processing pipeline. The pipeline contains various processing nodes. \n"
                                                                   "You need to analyze the user's data types and data content, and then recommend a pipeline accordingly. List the nodes (steps) included in the recommended pipeline, and explain why you are making this recommendation. "
                " - Please return the recommended pipeline as a flowchart, and generate the corresponding Mermaid code. \n"
                " - Example: {{\"mermaid\": \"flowchart TD A[Input: Only Question] --> B[Step 5: Answer Generation Algorithm<br>(Use strong reasoning model to generate Answer)] B --> C[Step 6: Format Filter<br>(Check <think> and <answer> tags)] C --> D[Step 7: Length Filter<br>(Remove answers that are truncated)] D --> E[Step 8: Answer Extraction Algorithm<br>(Extract final answer field)] E --> F[Step 9: Answer Filtering Algorithm<br>(Correctness matching / Reward scoring)] F --> G[Step 10: Deduplication<br>(N-gram deduplication)] G --> H[Output: High-quality Question-Answer Pairs]\"}}\n"
            ),

            'task_prompt_for_recommendation_inference_pipeline': (
                "Knowledge base content: {content}\n,"
                "Analyze the data types and status of this knowledge base. \n"
                "The available pipeline node details are as follows: "
                """[
    {{
        "step": 0,
        "name": "Question正确性Verify算法",
        "description": "对输入数据中的问题进行正确性验证，修正可能存在的错误，输出验证后的问题到新的文件中。"
    }},
    {{
        "step": 1,
        "name": "Question合成算法",
        "description": "根据验证后的问题，每个问题合成指定数量（这里是 5 条）的新问题，将合成的问题存储到新文件中。"
    }},
    {{
        "step": 2,
        "name": "Question正确性Verify算法",
        "description": "对合成的问题再次进行正确性验证，确保合成问题的质量，输出验证后的合成问题到新文件中。"
    }},
    {{
        "step": 3,
        "name": "Question难度分类",
        "description": "对验证后的合成问题进行难度分类，为每个问题添加难度标签，存储到新文件中。"
    }},
    {{
        "step": 4,
        "name": "Question类别分类器",
        "description": "对经过难度分类的问题进行类别分类，为每个问题添加类别标签，存储到新文件中。"
    }},
    {{
        "step": 5,
        "name": "合成数据伪答案生成器",
        "description": "为没有正确答案的问题生成伪答案，用于后续的筛选和处理。"
    }},
    {{
        "step": 6,
        "name": "规则过滤(格式过滤)",
        "description": "对答案进行格式过滤，统一答案的格式规则，需要与答案合成步骤对接。"
    }},
    {{
        "step": 7,
        "name": "规则过滤(长度过滤)",
        "description": "去除在最大令牌处截断的数据，保证答案的完整性。"
    }},
    {{
        "step": 8,
        "name": "Answer提取算法",
        "description": "从答案中提取正确答案，目前暂时不用。"
    }},
    {{
        "step": 9,
        "name": "Answer筛选算法",
        "description": "根据正确答案进行匹配，筛选出正确的答案。"
    }},
    {{
        "step": 10,
        "name": "规则过滤（去重）",
        "description": "使用 Ngram 方法去除连续重复的语法句，避免数据冗余。"
    }}
]"""
                " - You need to choose the appropriate steps based on the data type!"
                " - Generate Mermaid code based on the above nodes and Knowledge base content.\n"
            ),
        }

    def add_sys_template(self, name: str, template: str):
        """添加新的提示词模板"""
        self.templates[f"system_{name}"] = template

    def add_task_template(self, name: str, template: str):
        """添加新的提示词模板"""
        self.templates[f"task_{name}"] = template

    def render(self, template_name: str, **kwargs) -> str:
        """渲染指定模板，替换变量"""
        if template_name not in self.templates:
            raise ValueError(f"模板 '{template_name}' 不存在")

        return self.templates[template_name].format(**kwargs) + f".(Answer in {self.output_language}!!!);"

    def list_templates(self) -> list:
        """获取所有可用模板名称"""
        return list(self.templates.keys())
