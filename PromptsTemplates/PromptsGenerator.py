class PromptsTemplateGenerator:
    def __init__(self,output_language:str):
        self.output_language = output_language
        self.templates = {
            'system_prompts': (
                "You are a professional data analyst. "
            ),
            'task_summarize_template': (
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
            'dataflow_pipeline_recommendation': "",
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
