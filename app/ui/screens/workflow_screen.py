from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from ..widgets.step_item import StepItem
from ..theme import STEP_NAMES, STEP_DETAILS, hex_to_rgba

Builder.load_string('''
<WorkflowScreen>:
    canvas.before:
        Color:
            rgba: root.bg_color
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: [dp(8), dp(8)]
        spacing: dp(4)

        BoxLayout:
            size_hint_y: None
            height: dp(44)
            padding: [dp(4), dp(8)]
            Label:
                text: '生成流程'
                font_size: '18sp'
                bold: True
                color: root.text_color
                halign: 'left'
                valign: 'middle'
                text_size: self.size

        ScrollView:
            id: step_scroll
            do_scroll_x: False
            bar_width: dp(4)

            BoxLayout:
                id: step_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(4)
                padding: [dp(4), dp(4)]
''')


class WorkflowScreen(Screen):
    bg_color = ListProperty([0.941, 0.949, 0.961, 1.0])
    text_color = StringProperty('#1F2937')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_manager = None
        self._step_widgets = []
        Clock.schedule_once(lambda dt: self._build_steps(), 0.1)

    def _build_steps(self):
        if not hasattr(self, 'ids') or 'step_container' not in self.ids:
            Clock.schedule_once(lambda dt: self._build_steps(), 0.1)
            return

        container = self.ids.step_container
        container.clear_widgets()
        self._step_widgets = []

        for i in range(len(STEP_NAMES)):
            item = StepItem(
                step_index=i,
                step_name=STEP_NAMES[i],
                step_detail=STEP_DETAILS[i],
                status='pending',
            )
            if self.theme_manager:
                item.set_dark_mode(self.theme_manager.is_dark)
            container.add_widget(item)
            self._step_widgets.append(item)

    def set_step_status(self, index, status):
        if 0 <= index < len(self._step_widgets):
            self._step_widgets[index].status = status

    def set_step_running(self, index):
        self.set_step_status(index, 'running')

    def set_step_done(self, index):
        self.set_step_status(index, 'done')

    def set_step_error(self, index):
        self.set_step_status(index, 'error')

    def reset_all(self):
        for widget in self._step_widgets:
            widget.status = 'pending'

    def update_theme(self, colors):
        self.bg_color = hex_to_rgba(colors.get('bg_primary', '#F0F2F5'))
        self.text_color = colors.get('text_primary', '#1F2937')
        is_dark = self.bg_color == hex_to_rgba('#0F172A')
        for widget in self._step_widgets:
            widget.set_dark_mode(is_dark)
