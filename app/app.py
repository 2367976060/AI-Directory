from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.core.window import Window

from .config.settings_manager import SettingsManager
from .core.signal_bus import SignalBus
from .core.workflow_engine import WorkflowEngine
from .ui.theme import ThemeManager
from .ui.screens.main_screen import MainScreen
from .ui.screens.workflow_screen import WorkflowScreen
from .ui.screens.log_screen import LogScreen
from .ui.screens.settings_screen import SettingsScreen
from .ui.widgets.bottom_nav import BottomNav


class AIProjectGenerator(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = SettingsManager()
        self.signal_bus = SignalBus()
        self.theme_manager = ThemeManager()
        self.workflow_engine = None
        self._theme_applied = False

    def build(self):
        self.workflow_engine = WorkflowEngine(self.signal_bus)
        self.title = 'AI智能项目一键生成系统'

        # Root layout
        from kivy.uix.boxlayout import BoxLayout
        root = BoxLayout(orientation='vertical', spacing=0, padding=0)

        # Header
        from kivy.uix.label import Label
        header = Label(
            text='AI智能项目一键生成系统 v1.0.0',
            font_size='16sp',
            bold=True,
            color='#FFFFFF',
            size_hint_y=None,
            height=48,
        )
        with header.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.11, 0.16, 0.23, 1)
            self._header_rect = Rectangle(pos=header.pos, size=header.size)
            header.bind(pos=self._update_header_rect, size=self._update_header_rect)

        root.add_widget(header)

        # Screen manager
        sm = ScreenManager()
        self.main_screen = MainScreen(name='main')
        self.workflow_screen = WorkflowScreen(name='workflow')
        self.log_screen = LogScreen(name='log')
        self.settings_screen = SettingsScreen(name='settings')

        sm.add_widget(self.main_screen)
        sm.add_widget(self.workflow_screen)
        sm.add_widget(self.log_screen)
        sm.add_widget(self.settings_screen)

        root.add_widget(sm, 1)

        # Bottom navigation
        self.bottom_nav = BottomNav()
        self.bottom_nav.set_screen_manager(sm)
        self.bottom_nav.set_theme_manager(self.theme_manager)
        root.add_widget(self.bottom_nav)

        # Wire up shared references
        for screen in sm.screens:
            screen.app = self
            screen.signal_bus = self.signal_bus
            screen.settings = self.settings
            screen.theme_manager = self.theme_manager
            if hasattr(screen, 'workflow_engine'):
                screen.workflow_engine = self.workflow_engine

        # Connect signal bus
        self._connect_signals()

        return root

    def _update_header_rect(self, instance, value):
        self._header_rect.pos = instance.pos
        self._header_rect.size = instance.size

    def _connect_signals(self):
        sb = self.signal_bus
        sb.on('workflow_started', self._on_workflow_started)
        sb.on('workflow_completed', self._on_workflow_completed)
        sb.on('workflow_error', self._on_workflow_error)
        sb.on('workflow_log', self._on_workflow_log)
        sb.on('workflow_step_changed', self._on_step_changed)
        sb.on('workflow_progress', self._on_step_progress)
        sb.on('update_global_progress', self._on_global_progress)
        sb.on('cancel_requested', self._on_cancel_requested)

    def on_start(self):
        Clock.schedule_once(lambda dt: self._restore_settings(), 0.2)

    def _restore_settings(self):
        theme = self.settings.get('theme', 'light')
        if theme == 'dark':
            self.theme_manager.set_theme('dark')
            self._apply_theme()

    def _apply_theme(self):
        colors = self.theme_manager.colors
        self.main_screen.update_theme(colors)
        self.workflow_screen.update_theme(colors)
        self.log_screen.update_theme(colors)
        self.settings_screen.update_theme(colors)
        self.bottom_nav.update_theme(colors)

    def toggle_theme(self):
        self.theme_manager.toggle()
        self._apply_theme()
        self.settings.set('theme', self.theme_manager._current_theme)
        self.settings.save()

    # Signal handlers
    def _on_workflow_started(self, *args):
        self.main_screen.set_running(True)

    def _on_workflow_completed(self, success, output_path, *args):
        self.main_screen.set_running(False)
        if success and output_path:
            self.main_screen._output_path = output_path
            self.main_screen.set_output_available(True)
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            popup = Popup(
                title='完成',
                content=Label(text=f'项目生成完成！\n\n项目目录: {output_path}'),
                size_hint=(0.8, 0.4)
            )
            popup.open()
        else:
            self.main_screen.set_output_available(False)

    def _on_workflow_error(self, step_index, error_msg, *args):
        self.main_screen.set_running(False)
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(
            title='执行错误',
            content=Label(text=f'流程执行失败:\n{error_msg}'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def _on_workflow_log(self, level, message, *args):
        self.log_screen.add_log(level, message)

    def _on_step_changed(self, index, status, *args):
        self.workflow_screen.set_step_status(index, status)

    def _on_step_progress(self, step_index, percent, message, *args):
        self.main_screen.set_step_progress(percent, message)

    def _on_global_progress(self, percent, *args):
        self.main_screen.set_global_progress(percent)

    def _on_cancel_requested(self, *args):
        self.workflow_engine.cancel()

    def on_pause(self):
        return True

    def on_resume(self):
        pass
