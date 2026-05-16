from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from ..theme import hex_to_rgba

Builder.load_string('''
<StepItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(54)
    padding: [dp(12), dp(8)]
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: root.bg_color_rgba
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(6)]

    Label:
        id: icon_label
        text: root.icon_text
        font_size: '20sp'
        color: root.icon_color
        size_hint_x: None
        width: dp(32)
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(2)
        Label:
            text: root.step_name
            font_size: '13sp'
            bold: root.is_running
            color: root.name_color
            halign: 'left'
            valign: 'middle'
            text_size: self.size
            size_hint_y: 0.6
        Label:
            text: root.step_detail
            font_size: '10sp'
            color: root.detail_color
            halign: 'left'
            valign: 'top'
            text_size: self.size
            size_hint_y: 0.4
''')


class StepItem(BoxLayout):
    step_index = NumericProperty(0)
    step_name = StringProperty('')
    step_detail = StringProperty('')
    status = StringProperty('pending')
    icon_text = StringProperty('○')
    icon_color = StringProperty('#94A3B8')
    name_color = StringProperty('#1F2937')
    detail_color = StringProperty('#94A3B8')
    bg_color_rgba = ListProperty([1.0, 1.0, 1.0, 0.0])
    is_running = BooleanProperty(False)

    ICONS = {'pending': '○', 'running': '→', 'done': '●', 'error': '▲'}
    STATUS_COLORS = {
        'pending': '#94A3B8',
        'running': '#3B82F6',
        'done': '#10B981',
        'error': '#EF4444',
    }
    STATUS_BG = {
        'pending': 'transparent',
        'running': '#EFF6FF',
        'done': '#ECFDF5',
        'error': '#FEF2F2',
    }
    STATUS_BG_DARK = {
        'pending': 'transparent',
        'running': '#1E293B',
        'done': '#0F172A',
        'error': '#1E293B',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_dark = False
        self.bind(status=self._on_status_changed)

    def set_dark_mode(self, is_dark):
        self._is_dark = is_dark
        self._on_status_changed()

    def _on_status_changed(self, *args):
        self.icon_text = self.ICONS.get(self.status, '○')
        self.icon_color = self.STATUS_COLORS.get(self.status, '#94A3B8')
        self.name_color = self.STATUS_COLORS.get(self.status, '#1F2937')
        bg_dict = self.STATUS_BG_DARK if self._is_dark else self.STATUS_BG
        bg_hex = bg_dict.get(self.status, 'transparent')
        self.bg_color_rgba = hex_to_rgba(bg_hex) if bg_hex != 'transparent' else [1.0, 1.0, 1.0, 0.0]
        self.is_running = self.status == 'running'
