from ..step_base import AbstractStep


SYSTEM_PROMPT = """你是一位资深软件架构师。请根据需求分析文档，设计完整的项目架构方案。"""

USER_PROMPT_TEMPLATE = """请根据以下需求分析文档，设计完整的《项目架构设计方案》（使用Markdown格式）：

{requirements_doc}

请严格包含以下章节：
1. **整体架构设计** - 系统架构图描述（文字版）、分层架构、核心设计模式
2. **技术选型** - 前端技术、后端技术、数据库、中间件、第三方服务
3. **目录结构** - 完整的项目目录树结构
4. **运行逻辑** - 核心业务流程、数据流向、状态管理
5. **部署方式** - 开发环境、测试环境、生产环境部署方案
6. **层级关系** - 各模块之间的依赖关系和调用链路
7. **数据库设计** - 核心数据表结构设计（如适用）

要求：技术选型合理、架构清晰、可落地实现。"""


class Step02Architecture(AbstractStep):
    def __init__(self, step_index, context, project_manager, config):
        super().__init__(step_index, '整体项目架构规划设计', context, project_manager, config)

    def execute(self):
        req_doc = self.context.get('requirements_doc', '')
        if not req_doc:
            raise ValueError('缺少需求分析文档，无法进行架构设计')

        self._log('INFO', '正在分析需求文档并进行架构设计...')

        user_prompt = USER_PROMPT_TEMPLATE.format(requirements_doc=req_doc)
        response = self._call_ai(SYSTEM_PROMPT, user_prompt, 10, 90)

        self._log('INFO', '架构设计方案生成完成，正在整理...')

        self._write_output(None, '项目架构设计方案.md', response)

        self.context['architecture_doc'] = response

        self._log('INFO', '项目架构设计方案已保存')

        return self.context
