import os
from datetime import datetime
from ..step_base import AbstractStep

USAGE_TEMPLATE = """# 项目使用教程

## 项目名称
{project_name}

## 生成时间
{generate_time}

## 目录结构
```
{project_name}/
├── 01-需求分析/          # 需求分析文档
├── 02-架构设计/          # 项目架构设计方案
├── 03-模块拆分/          # 功能模块拆分文档
├── 04-源码生成/          # 完整项目源代码
│   └── source_code/      # 源码文件目录
├── 05-接口文档/          # API接口文档
├── 06-代码审查/          # 代码审查报告
└── 07-最终输出/          # 最终打包文件
```

## 环境配置

### 系统要求
- 操作系统：Windows 10/11, macOS, Linux
- 运行环境：根据项目技术栈安装对应环境

### 快速启动
1. 进入源码目录: `cd 04-源码生成/source_code`
2. 安装依赖: 参考项目中的配置文件
3. 启动项目: 参考项目中的启动脚本

## 运行说明
详见各步骤目录中的详细文档。
"""

STARTUP_TEMPLATE = """# 项目启动说明

## 环境要求
请根据项目技术栈安装相应的运行环境。

## 安装步骤
1. 打开终端/命令行
2. 进入源码目录
3. 按项目配置文件要求安装依赖
4. 配置环境变量（如有需要）

## 启动命令
根据项目技术栈选择合适的启动方式。

## 访问地址
启动后根据项目配置访问对应的地址和端口。

## 注意事项
- 确保所有依赖已正确安装
- 检查配置文件是否正确
- 确保端口未被占用
"""

ENV_TEMPLATE = """# 环境配置文件
# 复制此文件为 .env 并修改对应的配置值

# 应用配置
APP_NAME=generated_project
APP_ENV=development
APP_DEBUG=true
APP_PORT=8080

# 数据库配置（如适用）
DB_HOST=localhost
DB_PORT=3306
DB_NAME=myapp
DB_USER=root
DB_PASSWORD=

# 缓存配置（如适用）
REDIS_HOST=localhost
REDIS_PORT=6379
"""

GITIGNORE_TEMPLATE = """# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc
*.pyo

# Environment
.env
.env.local
*.log

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/
"""

README_TEMPLATE = """# {project_name}

## 项目简介
由AI智能项目一键生成系统自动生成的完整项目。

## 生成时间
{generate_time}

## 项目内容
- 📋 需求分析文档
- 🏗️ 项目架构设计方案
- 📦 功能模块拆分文档
- 💻 完整项目源代码
- 📚 API接口文档
- 🔍 代码审查报告

## 快速导航
- 需求分析：[01-需求分析/需求分析文档.md](../01-需求分析/需求分析文档.md)
- 架构设计：[02-架构设计/项目架构设计方案.md](../02-架构设计/项目架构设计方案.md)
- 源码目录：[04-源码生成/source_code/](../04-源码生成/source_code/)
- 接口文档：[05-接口文档/API接口文档.md](../05-接口文档/API接口文档.md)
- 审查报告：[06-代码审查/代码审查报告.md](../06-代码审查/代码审查报告.md)

## 使用说明
详见 `使用教程.md` 和 `启动说明.md` 文件。
"""


class Step07Package(AbstractStep):
    def __init__(self, step_index, context, project_manager, config):
        super().__init__(step_index, '全项目自动整理打包输出', context, project_manager, config)

    def execute(self):
        project_name = self.project_manager.project_name or 'AI生成项目'
        generate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._log('INFO', '正在整理项目文件...')
        self._progress(10, '正在分类整理所有文件...')

        self._generate_docs(project_name, generate_time)

        self._progress(40, '文档生成完成，正在打包...')

        zip_path = self.project_manager.create_output_zip()

        self._progress(80, '打包完成，正在准备输出...')

        output_dir = self.project_manager.project_dir / '07-最终输出'
        abs_zip_path = str(zip_path.absolute())

        self.context['output_path'] = str(self.project_manager.project_dir)
        self.context['zip_path'] = abs_zip_path
        self.context['output_dir'] = str(output_dir)

        self._log('INFO', f'项目文件已打包至: {abs_zip_path}')
        self._progress(100, f'项目打包完成: {abs_zip_path}')

        return self.context

    def _generate_docs(self, project_name, generate_time):
        self._log('INFO', '正在生成项目文档和说明文件...')

        output_dir = '07-最终输出'

        self._write_output(output_dir, '使用教程.md', USAGE_TEMPLATE.format(
            project_name=project_name,
            generate_time=generate_time
        ))
        self._log('INFO', '已生成: 使用教程.md')

        self._write_output(output_dir, '启动说明.md', STARTUP_TEMPLATE)
        self._log('INFO', '已生成: 启动说明.md')

        self._write_output(output_dir, 'env.example', ENV_TEMPLATE)
        self._log('INFO', '已生成: 环境配置模板')

        self._write_output(output_dir, '.gitignore', GITIGNORE_TEMPLATE)
        self._log('INFO', '已生成: .gitignore')

        self._write_output(output_dir, 'README.md', README_TEMPLATE.format(
            project_name=project_name,
            generate_time=generate_time
        ))
        self._log('INFO', '已生成: README.md')

        self._log('INFO', '项目文档生成完成')
