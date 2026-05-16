from ..step_base import AbstractStep


SYSTEM_PROMPT = """你是一位技术文档工程师。请根据项目源码，生成标准、完整的API接口文档。"""

USER_PROMPT_TEMPLATE = """请根据以下生成的源码和项目信息，编写标准API接口文档（使用Markdown格式）：

## 项目源码参考
{code_snippets}

## 需求分析
{requirements_doc}

## 架构设计
{architecture_doc}

请生成标准的API接口文档，严格包含以下章节：
1. **接口概览** - 接口清单、基础URL、认证方式
2. **接口详情（每个接口包含）**：
   - 接口名称
   - 请求方式 (GET/POST/PUT/DELETE)
   - 接口路径
   - 请求参数（参数名、类型、是否必填、说明）
   - 返回参数（参数名、类型、说明）
   - 请求示例（JSON格式）
   - 成功响应示例（JSON格式）
   - 错误响应示例
3. **错误码说明** - 全局错误码列表
4. **调用限制** - 频率限制、并发限制
5. **数据模型** - 核心数据模型定义

要求：格式标准通用（参考OpenAPI/Swagger风格）、描述清晰、示例完整。"""


class Step05Docs(AbstractStep):
    def __init__(self, step_index, context, project_manager, config):
        super().__init__(step_index, '统一接口文档自动编写', context, project_manager, config)

    def execute(self):
        req_doc = self.context.get('requirements_doc', '')
        arch_doc = self.context.get('architecture_doc', '')
        codegen = self.context.get('codegen_output', '')

        if not req_doc or not arch_doc:
            raise ValueError('缺少需求文档或架构设计，无法生成接口文档')

        code_snippets = codegen[:3000] if codegen else '（无源码参考）'
        self._log('INFO', '正在分析源码并生成接口文档...')

        user_prompt = USER_PROMPT_TEMPLATE.format(
            code_snippets=code_snippets,
            requirements_doc=req_doc,
            architecture_doc=arch_doc
        )
        response = self._call_ai(SYSTEM_PROMPT, user_prompt, 10, 90)

        self._log('INFO', '接口文档生成完成，正在整理...')

        self._write_output(None, 'API接口文档.md', response)

        self.context['api_doc'] = response

        self._log('INFO', 'API接口文档已保存')

        return self.context
