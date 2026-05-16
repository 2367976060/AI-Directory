from ..step_base import AbstractStep


SYSTEM_PROMPT = """你是一个专业的软件需求分析师。请严格分析以下用户需求，输出一份完整、规范、结构化的《需求分析文档》。"""

USER_PROMPT_TEMPLATE = """请分析以下项目需求，输出结构化的需求分析文档（使用Markdown格式）：

{user_requirement}

请严格包含以下章节：
1. **项目概述** - 项目背景、目标、核心价值
2. **功能需求列表** - 核心功能、扩展功能、功能优先级（高/中/低）
3. **非功能需求** - 性能要求、安全要求、可用性、兼容性
4. **用户角色** - 系统涉及的所有用户角色及其权限
5. **使用场景** - 典型使用场景和操作流程
6. **运行环境** - 推荐的技术栈、运行平台、部署环境
7. **开发方向** - 技术选型建议、开发路线图

要求：格式规范、条理清晰、描述精确。"""


class Step01Parse(AbstractStep):
    def __init__(self, step_index, context, project_manager, config):
        super().__init__(step_index, '需求智能解析整理', context, project_manager, config)

    def execute(self):
        user_input = self.context.get('input', '')
        if not user_input:
            raise ValueError('用户输入内容为空，无法进行需求分析')

        self._log('INFO', f'正在分析用户需求内容 (共{len(user_input)}字)...')

        user_prompt = USER_PROMPT_TEMPLATE.format(user_requirement=user_input)
        response = self._call_ai(SYSTEM_PROMPT, user_prompt, 10, 90)

        self._log('INFO', 'AI需求分析完成，正在整理文档...')

        self._write_output(None, '需求分析文档.md', response)

        self.context['requirements_doc'] = response
        self.context['requirements_summary'] = self._extract_summary(response)

        self._log('INFO', f'需求分析文档已保存')

        return self.context

    def _extract_summary(self, doc):
        lines = doc.split('\n')
        summary_lines = []
        in_summary = False
        for line in lines:
            if '项目概述' in line or '项目背景' in line:
                in_summary = True
            if in_summary:
                summary_lines.append(line)
                if len(summary_lines) >= 10:
                    break
        return '\n'.join(summary_lines)
