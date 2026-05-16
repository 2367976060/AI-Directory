from ..step_base import AbstractStep


SYSTEM_PROMPT = """你是一位全栈开发工程师。请根据项目架构和模块设计，生成完整的项目源码。生成的代码必须完整、规范、可直接运行。"""

USER_PROMPT_TEMPLATE = """请根据以下项目信息，生成完整的项目源码。

## 架构设计方案
{architecture_doc}

## 模块拆分文档
{modules_doc}

请生成以下完整源代码文件（使用Markdown格式，每个文件用 ``` 代码块包裹，标注文件路径）：

### 1. 后端代码
- 主应用入口文件 (如 main.py / app.js / main.go)
- 配置文件 (如 config.py / config.js)
- 路由定义文件
- 核心业务逻辑文件
- 数据模型/实体定义
- 工具类/辅助函数
- API接口实现

### 2. 前端代码（如适用）
- 入口文件
- 页面组件
- 路由配置
- API调用层
- UI组件

### 3. 配置和工具文件
- 数据库配置文件
- 日志配置
- 环境变量模板(.env.example)
- Dockerfile（如适用）

### 4. 启动脚本
- 开发环境启动脚本
- 生产环境启动脚本

要求：
1. 所有代码必须完整，不能有省略或"// TODO"占位符
2. 包含必要的import语句
3. 代码结构清晰，添加中文注释
4. 确保逻辑完整，可直接运行
5. 每个文件必须包含完整的内容

输出格式要求：
每个代码文件使用以下格式：
## 文件路径: [相对路径]
```[语言]
[完整代码内容]
```"""


class Step04Codegen(AbstractStep):
    def __init__(self, step_index, context, project_manager, config):
        super().__init__(step_index, '前后端完整源码智能生成', context, project_manager, config)

    def execute(self):
        arch_doc = self.context.get('architecture_doc', '')
        modules_doc = self.context.get('modules_doc', '')
        if not arch_doc or not modules_doc:
            raise ValueError('缺少架构设计或模块拆分文档，无法生成源码')

        self._log('INFO', '正在生成项目源码，此步骤可能需要较长时间...')

        user_prompt = USER_PROMPT_TEMPLATE.format(
            architecture_doc=arch_doc,
            modules_doc=modules_doc
        )
        response = self._call_ai(SYSTEM_PROMPT, user_prompt, 10, 85)

        self._log('INFO', '源码生成完成，正在解析和保存文件...')

        files_saved = self._parse_and_save_files(response)

        self.context['codegen_output'] = response
        self.context['generated_files'] = files_saved

        self._log('INFO', f'源码生成完成，共保存 {len(files_saved)} 个文件')

        return self.context

    def _parse_and_save_files(self, response):
        import re

        files_saved = []
        pattern = r'##\s*文件路径:\s*([^\n]+)\s*\n```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)

        for filepath, lang, content in matches:
            filepath = filepath.strip()
            content = content.strip()
            if not content:
                continue
            try:
                saved_path = self._write_output('source_code', filepath, content)
                files_saved.append(str(saved_path))
                self._log('INFO', f'已生成文件: {filepath}')
            except Exception as e:
                self._log('WARN', f'保存文件失败 {filepath}: {e}')

        if not files_saved:
            self._log('WARN', '未从AI响应中解析出代码文件，尝试备选方案...')
            self._write_output('source_code', 'generated_source.md', response)
            files_saved.append('generated_source.md')

        return files_saved
