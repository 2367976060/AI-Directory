from ..step_base import AbstractStep


SYSTEM_PROMPT = """你是一位高级软件项目经理。请根据架构设计方案，将项目拆分为独立功能模块，并搭建完整的项目文件目录体系。"""

USER_PROMPT_TEMPLATE = """请根据以下架构设计方案，进行功能模块拆分并搭建标准项目目录结构（使用Markdown格式）：

{architecture_doc}

请严格包含以下章节：
1. **功能模块列表** - 前端页面模块、后端业务模块、工具模块、配置模块、日志模块、权限模块
2. **模块详细说明** - 每个模块的功能职责、输入输出、依赖关系
3. **标准项目目录结构** - 完整的目录树，包含：
   - src/ 或 backend/ (后端源码目录)
   - frontend/ 或 web/ (前端源码目录)
   - config/ (配置目录)
   - docs/ (文档目录)
   - tests/ (测试目录)
   - scripts/ (工具脚本目录)
4. **模块接口定义** - 模块间通信方式、接口规范

要求：目录结构完整标准、模块划分合理、层次分明。"""


class Step03Modules(AbstractStep):
    def __init__(self, step_index, context, project_manager, config):
        super().__init__(step_index, '功能模块拆分与结构搭建', context, project_manager, config)

    def execute(self):
        arch_doc = self.context.get('architecture_doc', '')
        if not arch_doc:
            raise ValueError('缺少架构设计方案，无法进行模块拆分')

        self._log('INFO', '正在分析架构方案并进行模块拆分...')

        user_prompt = USER_PROMPT_TEMPLATE.format(architecture_doc=arch_doc)
        response = self._call_ai(SYSTEM_PROMPT, user_prompt, 10, 80)

        self._log('INFO', '模块划分完成，正在创建项目目录结构...')

        self._write_output(None, '功能模块拆分文档.md', response)

        self.context['modules_doc'] = response
        self.context['directory_structure'] = self._extract_directory_structure(response)

        self._log('INFO', '目录结构已创建完成')
        self._progress(100, '模块拆分与目录搭建完成')

        return self.context

    def _extract_directory_structure(self, doc):
        lines = doc.split('\n')
        dir_lines = []
        in_code = False
        for line in lines:
            if line.startswith('```'):
                in_code = not in_code
                if not in_code:
                    break
                continue
            if in_code:
                dir_lines.append(line)
        return '\n'.join(dir_lines)
