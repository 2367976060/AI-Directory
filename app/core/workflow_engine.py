"""Workflow engine using threading.Thread instead of QThread."""

import threading
from kivy.clock import Clock
from .signal_bus import SignalBus
from .project_manager import ProjectManager, STEP_DIR_NAMES
from .steps.step01_parse import Step01Parse
from .steps.step02_architecture import Step02Architecture
from .steps.step03_modules import Step03Modules
from .steps.step04_codegen import Step04Codegen
from .steps.step05_docs import Step05Docs
from .steps.step06_review import Step06Review
from .steps.step07_package import Step07Package

STEP_CLASSES = [
    Step01Parse,
    Step02Architecture,
    Step03Modules,
    Step04Codegen,
    Step05Docs,
    Step06Review,
    Step07Package,
]


class WorkflowEngine:
    def __init__(self, signal_bus=None):
        self.signal_bus = signal_bus or SignalBus()
        self._worker_thread = None
        self._cancelled = False
        self._current_step = None
        self._project_manager = None

    def start(self, input_text, config):
        if self._worker_thread and self._worker_thread.is_alive():
            return

        self._cancelled = False
        self._current_step = None
        self._project_manager = None

        self._worker_thread = threading.Thread(
            target=self._run_worker,
            args=(input_text, config),
            daemon=True
        )
        self._worker_thread.start()

    def cancel(self):
        self._cancelled = True
        if self._current_step:
            self._current_step.cancel()

    def _safe_emit(self, event_name, *args):
        Clock.schedule_once(lambda dt: self.signal_bus.emit(event_name, *args))

    def _on_step_cancelled(self):
        return self._cancelled

    def _on_step_progress(self, step_index, percent, message):
        self._safe_emit('workflow_progress', step_index, percent, message)
        global_pct = int((step_index * 100 + percent) / len(STEP_CLASSES))
        self._safe_emit('update_global_progress', global_pct)

    def _on_step_log(self, step_index, level, message):
        self._safe_emit('workflow_log', level, message)

    def _on_step_completed(self, step_index, success, result):
        status = 'done' if success else 'error'
        self._safe_emit('workflow_step_changed', step_index, status)

    def _run_worker(self, input_text, config):
        self._safe_emit('workflow_started')
        self._safe_emit('workflow_log', 'INFO', '工作流引擎已启动...')

        try:
            projects_root = config.get('projects_dir', '')
            if not projects_root:
                from ..config.settings_manager import SettingsManager
                settings = SettingsManager()
                projects_root = str(settings.projects_dir)

            self._project_manager = ProjectManager(projects_root)
            project_dir = self._project_manager.create_project()

            context = {
                'input': input_text,
                'project_dir': str(project_dir),
                'generated_files': [],
            }
            self._safe_emit('workflow_log', 'INFO', f'项目目录: {project_dir}')

            for i, StepClass in enumerate(STEP_CLASSES):
                if self._cancelled:
                    self._safe_emit('workflow_log', 'WARN', '工作流已被用户取消')
                    break

                step_name = f'步骤 {i+1}/{len(STEP_CLASSES)}'
                self._safe_emit('workflow_step_changed', i, 'running')
                self._safe_emit('workflow_log', 'INFO', f'{step_name}: {STEP_CLASSES[i].__name__} 开始...')

                step = StepClass(i, context, self._project_manager, config)
                step._on_progress = self._on_step_progress
                step._on_log = self._on_step_log
                step._on_completed = self._on_step_completed
                self._current_step = step

                try:
                    context = step.run()
                    if context is None and i > 0:
                        break
                except Exception as e:
                    self._safe_emit('workflow_step_changed', i, 'error')
                    self._safe_emit('workflow_error', i, str(e))
                    self._safe_emit('workflow_log', 'ERROR', f'步骤 {i+1} 执行失败: {e}')
                    self._safe_emit('workflow_completed', False, '')
                    return

                if self._cancelled:
                    break

            if not self._cancelled:
                output_path = context.get('output_path', str(project_dir)) if context else str(project_dir)
                self._safe_emit('update_global_progress', 100)
                self._safe_emit('workflow_log', 'SUCCESS', '所有步骤执行完成！')
                self._safe_emit('workflow_completed', True, output_path)
            else:
                self._safe_emit('workflow_completed', False, '')

        except Exception as e:
            self._safe_emit('workflow_log', 'ERROR', f'系统异常: {e}')
            self._safe_emit('workflow_completed', False, '')
