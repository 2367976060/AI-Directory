from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from datetime import datetime
from ..widgets.log_entry import LogEntry
from ..theme import hex_to_rgba

Builder.load_string('''
<LogScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: None
            height: dp(48)
            padding: [dp(12), dp(8)]
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: root.bg_color
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: '运行日志'
                font_size: '18sp'
                bold: True
                color: root.text_color
                halign: 'left'
                valign: 'middle'
                text_size: self.size
            Button:
                text: '清空日志'
                font_size: '12sp'
                size_hint_x: None
                width: dp(80)
                height: dp(32)
                background_normal: ''
                background_color: root.clear_btn_color
                color: '#FFFFFF'
                pos_hint: {'center_y': 0.5}
                on_release: root.clear_log()

        ScrollView:
            id: log_scroll
            do_scroll_x: False
            bar_width: dp(4)
            canvas.before:
                Color:
                    rgba: root.log_bg
                Rectangle:
                    pos: self.pos
                    size: self.size

            BoxLayout:
                id: log_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [dp(8), dp(4)]
                spacing: dp(1)
''')


class LogScreen(Screen):
    bg_color = ListProperty([0.941, 0.949, 0.961, 1.0])
    text_color = StringProperty('#1F2937')
    log_bg = ListProperty([0.059, 0.09, 0.137, 1.0])
    clear_btn_color = ListProperty([0.28, 0.33, 0.41, 1.0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._log_count = 0

    def add_log(self, level, message):
        Clock.schedule_once(lambda dt: self._do_add_log(level, message))

    def _do_add_log(self, level, message):
        if not hasattr(self, 'ids') or 'log_container' not in self.ids:
            return
        timestamp = datetime.now().strftime('%H:%M:%S')
        entry = LogEntry(
            level=level,
            message=message,
            timestamp_str=timestamp,
        )
        self.ids.log_container.add_widget(entry)
        self._log_count += 1

        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.05)

    def _scroll_to_bottom(self):
        if hasattr(self, 'ids') and 'log_scroll' in self.ids:
            self.ids.log_scroll.scroll_y = 0

    def clear_log(self):
        if hasattr(self, 'ids') and 'log_container' in self.ids:
            self.ids.log_container.clear_widgets()
            self._log_count = 0

    def update_theme(self, colors):
        self.bg_color = hex_to_rgba(colors.get('bg_primary', '#F0F2F5'))
        self.text_color = colors.get('text_primary', '#1F2937')
        self.log_bg = hex_to_rgba(colors.get('bg_log', '#0F172A'))
        self.clear_btn_color = hex_to_rgba(colors.get('bg_button_clear', '#475569'))
