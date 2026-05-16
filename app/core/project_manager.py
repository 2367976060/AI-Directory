import os
import shutil
from datetime import datetime
from pathlib import Path
from ..utils.zip_utils import create_zip

STEP_DIR_NAMES = [
    '01-需求分析',
    '02-架构设计',
    '03-模块拆分',
    '04-源码生成',
    '05-接口文档',
    '06-代码审查',
    '07-最终输出'
]


class ProjectManager:
    def __init__(self, projects_root):
        self._projects_root = Path(projects_root)
        self._project_dir = None
        self._project_name = None

    def create_project(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._project_name = f'project_{timestamp}'
        self._project_dir = self._projects_root / self._project_name
        self._project_dir.mkdir(parents=True, exist_ok=True)

        for dir_name in STEP_DIR_NAMES:
            (self._project_dir / dir_name).mkdir(parents=True, exist_ok=True)

        return self._project_dir

    def write_file(self, step_index, sub_dir, filename, content):
        step_dir = STEP_DIR_NAMES[step_index] if 0 <= step_index < len(STEP_DIR_NAMES) else f'step_{step_index:02d}'
        target_dir = self._project_dir / step_dir

        if sub_dir:
            target_dir = target_dir / sub_dir
            target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        from ..utils.file_utils import ensure_utf8
        content = ensure_utf8(content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return file_path

    def create_output_zip(self):
        output_dir = self._project_dir / '07-最终输出'
        output_dir.mkdir(parents=True, exist_ok=True)

        zip_path = output_dir / f'{self._project_name}.zip'
        create_zip(self._project_dir, zip_path, exclude_dirs={'__pycache__', '.git'})
        return zip_path

    def open_in_explorer(self, path=None):
        target = path or str(self._project_dir)
        try:
            import subprocess, sys
            if sys.platform == 'android':
                pass
            elif sys.platform == 'win32':
                os.startfile(target)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', target])
            else:
                subprocess.Popen(['xdg-open', target])
        except Exception:
            pass

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def project_name(self):
        return self._project_name

    def cleanup(self):
        if self._project_dir and self._project_dir.exists():
            shutil.rmtree(self._project_dir)
