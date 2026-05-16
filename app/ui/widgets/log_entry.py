from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty

Builder.load_string('''
<LogEntry>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(22)
    padding: [dp(4), dp(1)]
    spacing: dp(6)

    Label:
        text: root.timestamp_str
        font_size: '10sp'
        font_name: 'monospace'
        color: root.ts_color
        size_hint_x: None
        width: dp(68)
        halign: 'left'
        valign: 'middle'
        text_size: self.size
    Label:
        text: root.prefix
        font_size: '10sp'
        bold: True
        color: root.level_color
        size_hint_x: None
        width: dp(42)
        halign: 'center'
        valign: 'middle'
        text_size: self.size
    Label:
        text: root.message
        font_size: '10sp'
        font_name: 'monospace'
        color: root.msg_color
        halign: 'left'
        valign: 'middle'
        text_size: self.size, None
        size_hint_y: None
        height: self.texture_size[1]
''')


class LogEntry(BoxLayout):
    level = StringProperty('INFO')
    message = StringProperty('')
    timestamp_str = StringProperty('')
    level_color = StringProperty('#CBD5E1')
    msg_color = StringProperty('#CBD5E1')
    ts_color = StringProperty('#6C7086')
    prefix = StringProperty('[Info]')
    index = NumericProperty(0)

    LEVEL_PREFIX = {
        'INFO': '[Info]',
        'SUCCESS': '[Success]',
        'WARN': '[Warning]',
        'ERROR': '[Error]',
        'DEBUG': '[Debug]',
    }

    LEVEL_COLORS = {
        'INFO': '#D4D4D4',
        'SUCCESS': '#27AE60',
        'WARN': '#F39C12',
        'ERROR': '#E74C3C',
        'DEBUG': '#888888',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(level=self._update_colors)

    def _update_colors(self, *args):
        self.prefix = self.LEVEL_PREFIX.get(self.level, '[Info]')
        self.level_color = self.LEVEL_COLORS.get(self.level, '#D4D4D4')
        self.msg_color = self.LEVEL_COLORS.get(self.level, '#D4D4D4')
