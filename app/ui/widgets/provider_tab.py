from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty

Builder.load_string('''
<ProviderTab>:
    orientation: 'vertical'
    padding: [dp(16), dp(12)]
    spacing: dp(10)

    Label:
        text: 'API密钥'
        font_size: '13sp'
        color: root.label_color
        size_hint_y: None
        height: dp(20)
        halign: 'left'
        text_size: self.size
    TextInput:
        id: api_key
        hint_text: root.api_key_hint
        password: True
        password_mask: '*'
        font_size: '14sp'
        multiline: False
        size_hint_y: None
        height: dp(42)
        foreground_color: root.input_fg
        background_color: root.input_bg
        hint_text_color: root.hint_color

    Label:
        text: '接口地址'
        font_size: '13sp'
        color: root.label_color
        size_hint_y: None
        height: dp(20)
        halign: 'left'
        text_size: self.size
    TextInput:
        id: base_url
        hint_text: root.base_url_hint
        font_size: '14sp'
        multiline: False
        size_hint_y: None
        height: dp(42)
        foreground_color: root.input_fg
        background_color: root.input_bg
        hint_text_color: root.hint_color

    Label:
        text: '模型名称'
        font_size: '13sp'
        color: root.label_color
        size_hint_y: None
        height: dp(20)
        halign: 'left'
        text_size: self.size
    Spinner:
        id: model_spinner
        text: root.model_items[0] if root.model_items else ''
        values: root.model_items
        font_size: '14sp'
        size_hint_y: None
        height: dp(42)
        foreground_color: root.input_fg
        background_color: root.input_bg

    Widget:
        size_hint_y: None
        height: dp(8)

    Button:
        id: test_btn
        text: '测试连接'
        font_size: '14sp'
        background_normal: ''
        background_color: root.test_btn_color
        color: '#FFFFFF'
        size_hint_y: None
        height: dp(44)
        on_release: root.test_callback()
        disabled: root.testing
''')


class ProviderTab(BoxLayout):
    provider_key = StringProperty('openai_compat')
    api_key_hint = StringProperty('sk-...')
    base_url_hint = StringProperty('https://api.openai.com/v1')
    model_items = ListProperty(['gpt-4o', 'gpt-4o-mini'])
    label_color = StringProperty('#1F2937')
    input_fg = StringProperty('#1F2937')
    input_bg = StringProperty('#FAFBFC')
    hint_color = StringProperty('#9CA3AF')
    test_btn_color = StringProperty('#10B981')
    testing = ObjectProperty(False)
    test_callback = ObjectProperty(lambda: None)

    def get_config(self):
        return {
            'api_key': self.ids.api_key.text if hasattr(self, 'ids') else '',
            'base_url': self.ids.base_url.text if hasattr(self, 'ids') else '',
            'model': self.ids.model_spinner.text if hasattr(self, 'ids') else '',
        }

    def set_config(self, config):
        if hasattr(self, 'ids'):
            self.ids.api_key.text = config.get('api_key', '')
            self.ids.base_url.text = config.get('base_url', self.base_url_hint)
            model = config.get('model', self.model_items[0] if self.model_items else '')
            if model in self.model_items:
                self.ids.model_spinner.text = model
            else:
                self.ids.model_spinner.text = model

    def set_testing(self, testing):
        self.testing = testing
        if hasattr(self, 'ids'):
            self.ids.test_btn.text = '测试中...' if testing else '测试连接'
            self.ids.test_btn.disabled = testing

    def update_theme(self, colors, is_dark):
        self.label_color = colors.get('text_primary', '#1F2937')
        self.input_fg = colors.get('text_primary', '#1F2937')
        self.input_bg = colors.get('bg_input', '#FAFBFC')
        self.hint_color = colors.get('text_muted', '#9CA3AF')
        self.test_btn_color = colors.get('bg_button_test', '#10B981')
