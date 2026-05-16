from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from ..theme import hex_to_rgba

Builder.load_string('''
<NavButton>:
    font_size: '11sp'
    size_hint_x: 1
    background_normal: ''
    background_color: root.my_bg
    color: root.my_color
    markup: True

<BottomNav>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(56)
    padding: [dp(4), dp(4)]
    spacing: dp(2)
    canvas.before:
        Color:
            rgba: root.border_rgba
        Rectangle:
            pos: self.x, self.top - dp(1)
            size: self.width, dp(1)
        Color:
            rgba: root.bg_rgba
        Rectangle:
            pos: self.pos
            size: self.size

    NavButton:
        id: btn_main
        text: '[b]主界面[/b]\\n✏️'
        my_bg: root.active_rgba if root.current == 'main' else root.inactive_rgba
        my_color: root.active_text_color if root.current == 'main' else root.inactive_text_color
        on_release: root.switch_to('main')
    NavButton:
        id: btn_workflow
        text: '[b]工作流[/b]\\n📋'
        my_bg: root.active_rgba if root.current == 'workflow' else root.inactive_rgba
        my_color: root.active_text_color if root.current == 'workflow' else root.inactive_text_color
        on_release: root.switch_to('workflow')
    NavButton:
        id: btn_log
        text: '[b]日志[/b]\\n📝'
        my_bg: root.active_rgba if root.current == 'log' else root.inactive_rgba
        my_color: root.active_text_color if root.current == 'log' else root.inactive_text_color
        on_release: root.switch_to('log')
    NavButton:
        id: btn_settings
        text: '[b]设置[/b]\\n⚙️'
        my_bg: root.active_rgba if root.current == 'settings' else root.inactive_rgba
        my_color: root.active_text_color if root.current == 'settings' else root.inactive_text_color
        on_release: root.switch_to('settings')
''')


class NavButton(Button):
    my_bg = ListProperty([1.0, 1.0, 1.0, 0.0])
    my_color = StringProperty('#94A3B8')


class BottomNav(BoxLayout):
    current = StringProperty('main')
    bg_rgba = ListProperty([1.0, 1.0, 1.0, 1.0])
    border_rgba = ListProperty([0.886, 0.91, 0.941, 1.0])
    active_rgba = ListProperty([0.878, 0.906, 1.0, 1.0])
    inactive_rgba = ListProperty([1.0, 1.0, 1.0, 0.0])
    active_text_color = StringProperty('#4F46E5')
    inactive_text_color = StringProperty('#94A3B8')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._screen_manager = None
        self._theme_manager = None

    def set_screen_manager(self, sm):
        self._screen_manager = sm

    def set_theme_manager(self, tm):
        self._theme_manager = tm

    def update_theme(self, colors):
        self.bg_rgba = hex_to_rgba(colors.get('bg_nav', '#FFFFFF'))
        self.border_rgba = hex_to_rgba(colors.get('border', '#E2E8F0'))
        is_dark = self._theme_manager.is_dark if self._theme_manager else False
        self.active_rgba = hex_to_rgba('#E0E7FF') if not is_dark else hex_to_rgba('#312E81')
        self.inactive_rgba = [1.0, 1.0, 1.0, 0.0]
        self.active_text_color = '#4F46E5' if not is_dark else '#A5B4FC'
        self.inactive_text_color = colors.get('text_muted', '#94A3B8')

    def switch_to(self, screen_name):
        self.current = screen_name
        if self._screen_manager:
            self._screen_manager.current = screen_name
