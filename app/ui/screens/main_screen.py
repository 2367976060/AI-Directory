from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ListProperty
from ..theme import hex_to_rgba

Builder.load_string('''
<MainScreen>:
    canvas.before:
        Color:
            rgba: root.bg_color
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: [dp(12), dp(8)]
        spacing: dp(6)

        # Title row with char count
        BoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: dp(8)
            Label:
                text: '输入项目需求'
                font_size: '17sp'
                bold: True
                color: root.text_color
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                size_hint_x: 0.7
            Label:
                id: char_count
                text: '0 字符'
                font_size: '11sp'
                color: root.char_color
                size_hint_x: 0.3
                halign: 'right'
                valign: 'middle'
                text_size: self.size

        # Input text area
        TextInput:
            id: input_area
            hint_text: '详细描述您的项目需求...\\n\\n例如：开发一个在线图书管理系统，支持用户注册登录、\\n图书搜索、借书还书、管理员后台管理等。使用Python + Vue开发。\\n\\n提示：描述越详细，生成的项目越精准。'
            text: ''
            multiline: True
            font_size: '14sp'
            foreground_color: root.input_fg
            background_color: root.input_bg
            padding: [dp(8), dp(8)]
            size_hint_y: 0.4
            on_text: root.on_text_changed(self.text)

        # Global progress
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            orientation: 'vertical'
            spacing: dp(2)
            BoxLayout:
                size_hint_y: None
                height: dp(18)
                Label:
                    text: '总进度'
                    font_size: '12sp'
                    color: root.text_color
                    halign: 'left'
                    text_size: self.size
                Label:
                    id: global_pct
                    text: '0%'
                    font_size: '11sp'
                    color: root.pct_color
                    size_hint_x: None
                    width: dp(44)
                    halign: 'right'
            ProgressBar:
                id: global_bar
                max: 100
                value: 0
                size_hint_y: None
                height: dp(10)

        # Step progress
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            orientation: 'vertical'
            spacing: dp(2)
            BoxLayout:
                size_hint_y: None
                height: dp(18)
                Label:
                    id: step_label
                    text: '当前步骤'
                    font_size: '12sp'
                    color: root.text_color
                    halign: 'left'
                    text_size: self.size
                Label:
                    id: step_pct
                    text: '0%'
                    font_size: '11sp'
                    color: root.pct_color
                    size_hint_x: None
                    width: dp(44)
                    halign: 'right'
            ProgressBar:
                id: step_bar
                max: 100
                value: 0
                size_hint_y: None
                height: dp(10)

        # Action buttons
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(8)
            padding: [dp(0), dp(4)]
            Button:
                id: btn_start
                text: '开始生成'
                font_size: '14sp'
                bold: True
                background_normal: ''
                background_color: root.start_btn_color
                color: '#FFFFFF'
                on_release: root.on_start()
            Button:
                id: btn_stop
                text: '停止'
                font_size: '14sp'
                background_normal: ''
                background_color: root.stop_btn_color
                color: '#FFFFFF'
                disabled: True
                on_release: root.on_stop()
            Button:
                id: btn_clear
                text: '清空'
                font_size: '14sp'
                background_normal: ''
                background_color: root.clear_btn_color
                color: '#FFFFFF'
                on_release: root.on_clear()
            Button:
                id: btn_open
                text: '打开目录'
                font_size: '14sp'
                background_normal: ''
                background_color: root.open_btn_color
                color: '#FFFFFF'
                disabled: True
                on_release: root.on_open_dir()

        Widget:
            size_hint_y: 0.05
''')


class MainScreen(Screen):
    bg_color = ListProperty([0.941, 0.949, 0.961, 1.0])
    text_color = StringProperty('#1F2937')
    input_fg = StringProperty('#1F2937')
    input_bg = ListProperty([0.98, 0.984, 0.988, 1.0])
    char_color = StringProperty('#9CA3AF')
    pct_color = StringProperty('#6B7280')
    start_btn_color = ListProperty([0.022, 0.588, 0.412, 1.0])
    stop_btn_color = ListProperty([0.863, 0.149, 0.149, 1.0])
    clear_btn_color = ListProperty([0.42, 0.44, 0.49, 1.0])
    open_btn_color = ListProperty([0.231, 0.51, 0.965, 1.0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.signal_bus = None
        self.settings = None
        self.theme_manager = None
        self.workflow_engine = None
        self._is_running = False
        self._output_path = ''

    def on_text_changed(self, text):
        count = len(text)
        if hasattr(self, 'ids') and 'char_count' in self.ids:
            self.ids.char_count.text = f'{count} 字符'
            if count > 10000:
                self.char_color = '#EF4444'
            elif count > 5000:
                self.char_color = '#F59E0B'
            else:
                self.char_color = '#9CA3AF'

    def on_start(self):
        if not hasattr(self, 'ids'):
            return
        input_text = self.ids.input_area.text.strip()
        if not input_text:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            popup = Popup(title='提示', content=Label(text='请输入项目需求内容后再开始生成！'),
                          size_hint=(0.7, 0.3))
            popup.open()
            return

        config = self.settings.get_all() if self.settings else {}
        provider_config = config.get('providers', {}).get(
            config.get('current_provider', 'openai_compat'), {}
        )
        if not provider_config.get('api_key'):
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.button import Button
            content = BoxLayout(orientation='vertical', spacing=10)
            content.add_widget(Label(text='未配置API密钥，是否前往设置？'))
            btn_layout = BoxLayout(size_hint_y=None, height=44, spacing=8)
            btn_yes = Button(text='是')
            btn_no = Button(text='否')
            btn_layout.add_widget(btn_yes)
            btn_layout.add_widget(btn_no)
            content.add_widget(btn_layout)
            popup = Popup(title='确认', content=content, size_hint=(0.7, 0.35))
            btn_yes.bind(on_release=lambda *a: [popup.dismiss(), self._open_settings()])
            btn_no.bind(on_release=popup.dismiss)
            popup.open()
            return

        self._is_running = True
        self._output_path = ''
        self.ids.btn_start.disabled = True
        self.ids.btn_stop.disabled = False
        self.ids.btn_clear.disabled = True
        self.ids.btn_open.disabled = True
        self._safe_add_log('INFO', '开始生成项目...')

        if self.signal_bus:
            self.signal_bus.start_requested(input_text, config)

    def _open_settings(self):
        if self.app and hasattr(self.app, 'root'):
            sm = self.app.root
            if sm and hasattr(sm, 'current'):
                sm.current = 'settings'

    def on_stop(self):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button

        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text='确定要停止当前生成任务吗？\n已生成的内容将保留。'))
        btn_layout = BoxLayout(size_hint_y=None, height=44, spacing=8)
        btn_yes = Button(text='确定')
        btn_no = Button(text='取消')
        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
        content.add_widget(btn_layout)
        popup = Popup(title='确认停止', content=content, size_hint=(0.7, 0.35))
        btn_yes.bind(on_release=lambda *a: [popup.dismiss(), self._do_stop()])
        btn_no.bind(on_release=popup.dismiss)
        popup.open()

    def _do_stop(self):
        if self.signal_bus:
            self.signal_bus.cancel_requested()

    def on_clear(self):
        if hasattr(self, 'ids'):
            self.ids.input_area.text = ''
            self.ids.global_bar.value = 0
            self.ids.step_bar.value = 0
            self.ids.global_pct.text = '0%'
            self.ids.step_pct.text = '0%'
            self.ids.step_label.text = '当前步骤'
        self._output_path = ''

    def on_open_dir(self):
        if self._output_path:
            try:
                import subprocess, sys, os
                if sys.platform == 'android':
                    self._safe_add_log('INFO', f'项目目录: {self._output_path}')
                elif sys.platform == 'win32':
                    os.startfile(self._output_path)
                elif sys.platform == 'darwin':
                    subprocess.Popen(['open', self._output_path])
                else:
                    subprocess.Popen(['xdg-open', self._output_path])
            except Exception as e:
                self._safe_add_log('ERROR', f'无法打开目录: {e}')

    def set_running(self, running):
        self._is_running = running
        if hasattr(self, 'ids'):
            self.ids.btn_start.disabled = running
            self.ids.btn_stop.disabled = not running
            self.ids.btn_clear.disabled = running

    def set_output_available(self, available):
        if hasattr(self, 'ids'):
            self.ids.btn_open.disabled = not available

    def set_global_progress(self, value):
        if hasattr(self, 'ids'):
            self.ids.global_bar.value = value
            self.ids.global_pct.text = f'{value}%'

    def set_step_progress(self, value, message=''):
        if hasattr(self, 'ids'):
            self.ids.step_bar.value = value
            self.ids.step_pct.text = f'{value}%'
            if message:
                self.ids.step_label.text = f'当前: {message}'
            else:
                self.ids.step_label.text = '当前步骤'

    def _safe_add_log(self, level, message):
        Clock.schedule_once(lambda dt: self._do_add_log(level, message))

    def _do_add_log(self, level, message):
        if self.signal_bus:
            self.signal_bus.log_message(level, message)

    def update_theme(self, colors):
        self.bg_color = hex_to_rgba(colors.get('bg_primary', '#F0F2F5'))
        self.text_color = colors.get('text_primary', '#1F2937')
        self.input_fg = colors.get('text_primary', '#1F2937')
        self.input_bg = hex_to_rgba(colors.get('bg_input', '#FAFBFC'))
        self.pct_color = colors.get('text_muted', '#6B7280')
        self.start_btn_color = hex_to_rgba(colors.get('bg_button_start', '#059669'))
        self.stop_btn_color = hex_to_rgba(colors.get('bg_button_stop', '#DC2626'))
        self.clear_btn_color = hex_to_rgba(colors.get('bg_button_clear', '#6B7280'))
        self.open_btn_color = hex_to_rgba(colors.get('bg_button_open', '#3B82F6'))
