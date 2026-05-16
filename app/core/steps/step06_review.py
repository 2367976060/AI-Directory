from ..step_base import AbstractStep


SYSTEM_PROMPT = """你是一位高级代码审查工程师。请对以下项目源码进行全面审查，找出问题并提供优化建议。"""

USER_PROMPT_TEMPLATE = """请对以下项目源码进行全面审查（使用Markdown格式）：

## 需求文档
{requirements_doc}

## 架构设计
{architecture_doc}

## 生成源码
{generated_code}

请严格包含以下审查内容：
1. **语法检测** - 检查所有源文件的语法错误、拼写错误
2. **逻辑排查** - 检查业务逻辑缺陷、空指针、边界条件
3. **安全检测** - 检查常见安全漏洞（SQL注入、XSS、CSRF、敏感信息泄露）
4. **格式优化** - 代码风格一致性、命名规范、缩进格式
5. **冗余清理** - 无用代码、重复代码、死代码、未使用的import
6. **依赖检查** - 缺失的import、版本兼容性
7. **报错风险** - 潜在运行时错误、异常处理缺失
8. **优化建议** - 性能优化、代码重构建议

对于发现的问题，请分类为：
- 🔴 严重错误（必须修复）
- 🟡 警告（建议修复）
- 🔵 优化建议（可选的改进）

输出格式要求：
```markdown
# 代码审查报告
## 1. 语法检测
...
## 2. 逻辑排查
...
```

请在报告最后输出修正后的完整代码（如果发现严重错误）。"""


class Step06Review(AbstractStep):
    def __init__(self, step_index, context, project_manager, config):
        super().__init__(step_index, '代码自检优化与错误排查', context, project_manager, config)

    def execute(self):
        req_doc = self.context.get('requirements_doc', '')
        arch_doc = self.context.get('architecture_doc', '')
        codegen = self.context.get('codegen_output', '')
        generated_files = self.context.get('generated_files', [])

        self._log('INFO', f'正在审查 {len(generated_files)} 个生成的文件...')

        generated_code = codegen[:5000] if codegen else '（无源码）'

        user_prompt = USER_PROMPT_TEMPLATE.format(
            requirements_doc=req_doc[:1000],
            architecture_doc=arch_doc[:1000],
            generated_code=generated_code
        )
        response = self._call_ai(SYSTEM_PROMPT, user_prompt, 10, 85)

        self._log('INFO', '代码审查完成，正在整理审查报告...')

        self._write_output(None, '代码审查报告.md', response)

        self.context['review_report'] = response

        self._log('INFO', '代码审查报告已保存')

        return self.context
