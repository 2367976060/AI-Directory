from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
import threading
from ..widgets.provider_tab import ProviderTab
from ...ai.client_factory import create_client_by_provider
from ..theme import hex_to_rgba

Builder.load_string('''
<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'

        # Title bar
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: [dp(12), dp(8)]
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: root.bg_color
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: '模型设置'
                font_size: '20sp'
                bold: True
                color: root.text_color
                halign: 'left'
                valign: 'middle'
                text_size: self.size

        # Tabbed panel
        TabbedPanel:
            id: provider_tabs
            do_default_tab: False
            tab_height: dp(44)
            background_color: root.tab_bg
            background_image: ''
            canvas.before:
                Color:
                    rgba: root.bg_color
                Rectangle:
                    pos: self.pos
                    size: self.size

            TabbedPanelHeader:
                text: 'OpenAI'
                font_size: '13sp'
                background_normal: ''
                background_color: root.tab_normal_bg
                color: root.tab_normal_text
            ProviderTab:
                id: openai_tab
                provider_key: 'openai_compat'
                api_key_hint: 'sk-...'
                base_url_hint: 'https://api.openai.com/v1'
                model_items: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo']

            TabbedPanelHeader:
                text: 'DeepSeek'
                font_size: '13sp'
                background_normal: ''
                background_color: root.tab_normal_bg
                color: root.tab_normal_text
            ProviderTab:
                id: deepseek_tab
                provider_key: 'deepseek'
                api_key_hint: 'sk-...'
                base_url_hint: 'https://api.deepseek.com'
                model_items: ['deepseek-chat', 'deepseek-reasoner', 'deepseek-coder']

            TabbedPanelHeader:
                text: 'Claude'
                font_size: '13sp'
                background_normal: ''
                background_color: root.tab_normal_bg
                color: root.tab_normal_text
            ProviderTab:
                id: anthropic_tab
                provider_key: 'anthropic'
                api_key_hint: 'sk-ant-...'
                base_url_hint: 'https://api.anthropic.com'
                model_items: ['claude-sonnet-4-20250514', 'claude-3-5-sonnet-20241022']

            TabbedPanelHeader:
                text: '高级参数'
                font_size: '13sp'
                background_normal: ''
                background_color: root.tab_normal_bg
                color: root.tab_normal_text
            BoxLayout:
                orientation: 'vertical'
                padding: [dp(16), dp(12)]
                spacing: dp(12)
                canvas.before:
                    Color:
                        rgba: root.bg_color
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: 'Temperature: {:.1f}'.format(root.temperature)
                    font_size: '13sp'
                    color: root.text_color
                    size_hint_y: None
                    height: dp(20)
                Slider:
                    id: temp_slider
                    min: 0.0
                    max: 2.0
                    step: 0.1
                    value: root.temperature
                    size_hint_y: None
                    height: dp(30)
                    value_track_width: dp(2)
                    on_value: root.temperature = self.value
                Label:
                    text: 'Max Tokens: {:d}'.format(root.max_tokens)
                    font_size: '13sp'
                    color: root.text_color
                    size_hint_y: None
                    height: dp(20)
                Slider:
                    id: tokens_slider
                    min: 256
                    max: 128000
                    step: 256
                    value: root.max_tokens
                    size_hint_y: None
                    height: dp(30)
                    value_track_width: dp(2)
                    on_value: root.max_tokens = int(self.value)
                Label:
                    text: 'Timeout: {:d}s'.format(root.timeout)
                    font_size: '13sp'
                    color: root.text_color
                    size_hint_y: None
                    height: dp(20)
                Slider:
                    id: timeout_slider
                    min: 30
                    max: 600
                    step: 10
                    value: root.timeout
                    size_hint_y: None
                    height: dp(30)
                    value_track_width: dp(2)
                    on_value: root.timeout = int(self.value)
                Label:
                    text: 'Max Retries: {:d}'.format(root.max_retries)
                    font_size: '13sp'
                    color: root.text_color
                    size_hint_y: None
                    height: dp(20)
                Slider:
                    id: retries_slider
                    min: 0
                    max: 10
                    step: 1
                    value: root.max_retries
                    size_hint_y: None
                    height: dp(30)
                    value_track_width: dp(2)
                    on_value: root.max_retries = int(self.value)

        # Bottom action bar
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            spacing: dp(8)
            padding: [dp(16), dp(8)]
            canvas.before:
                Color:
                    rgba: root.bg_color
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: '保存设置'
                font_size: '15sp'
                bold: True
                background_normal: ''
                background_color: root.save_btn_color
                color: '#FFFFFF'
                on_release: root.save_settings()
            Button:
                text: '取消'
                font_size: '15sp'
                background_normal: ''
                background_color: root.cancel_btn_color
                color: root.cancel_text_color
                on_release: root.go_back()
''')


class SettingsScreen(Screen):
    bg_color = ListProperty([0.941, 0.949, 0.961, 1.0])
    text_color = StringProperty('#1F2937')
    tab_bg = ListProperty([1.0, 1.0, 1.0, 1.0])
    tab_normal_bg = ListProperty([0.886, 0.91, 0.941, 1.0])
    tab_normal_text = StringProperty('#64748B')
    save_btn_color = ListProperty([0.231, 0.51, 0.965, 1.0])
    cancel_btn_color = ListProperty([0.898, 0.906, 0.922, 1.0])
    cancel_text_color = StringProperty('#374151')
    temperature = NumericProperty(0.7)
    max_tokens = NumericProperty(4096)
    timeout = NumericProperty(120)
    max_retries = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.settings = None
        self.signal_bus = None
        self.theme_manager = None

    def on_enter(self):
        Clock.schedule_once(lambda dt: self._load_config(), 0.1)
        Clock.schedule_once(lambda dt: self._wire_callbacks(), 0.2)

    def _wire_callbacks(self):
        if not hasattr(self, 'ids'):
            return
        for provider_key, tab_id in [('openai_compat', 'openai_tab'),
                                      ('deepseek', 'deepseek_tab'),
                                      ('anthropic', 'anthropic_tab')]:
            if tab_id in self.ids:
                self.ids[tab_id].test_callback = lambda k=provider_key: self.run_test(k)

    def _load_config(self):
        if not self.settings:
            return
        config = self.settings.get_all()

        providers_config = config.get('providers', {})
        if hasattr(self, 'ids'):
            for provider_key, tab_id in [('openai_compat', 'openai_tab'),
                                          ('deepseek', 'deepseek_tab'),
                                          ('anthropic', 'anthropic_tab')]:
                if tab_id in self.ids:
                    tab = self.ids[tab_id]
                    if hasattr(tab, 'set_config'):
                        tab.set_config(providers_config.get(provider_key, {}))

            adv = providers_config.get(config.get('current_provider', 'openai_compat'), {})
            self.temperature = adv.get('temperature', 0.7)
            self.max_tokens = adv.get('max_tokens', 4096)
            self.timeout = adv.get('timeout', 120)
            self.max_retries = adv.get('max_retries', 3)

    def save_settings(self):
        if not self.settings:
            return

        if hasattr(self, 'ids'):
            for provider_key, tab_id in [('openai_compat', 'openai_tab'),
                                          ('deepseek', 'deepseek_tab'),
                                          ('anthropic', 'anthropic_tab')]:
                if tab_id in self.ids:
                    tab = self.ids[tab_id]
                    if hasattr(tab, 'get_config'):
                        cfg = tab.get_config()
                        self.settings.set_provider_config(provider_key, cfg)

            for provider in ('openai_compat', 'deepseek', 'anthropic', 'custom'):
                self.settings.set(f'providers.{provider}.temperature', round(self.temperature, 1))
                self.settings.set(f'providers.{provider}.max_tokens', int(self.max_tokens))
                self.settings.set(f'providers.{provider}.timeout', int(self.timeout))
                self.settings.set(f'providers.{provider}.max_retries', int(self.max_retries))

        self.settings.save()
        if self.signal_bus:
            self.signal_bus.settings_changed(self.settings.get_all())

        self.go_back()

    def go_back(self):
        if self.app and hasattr(self.app, 'root'):
            sm = self.app.root
            if sm and hasattr(sm, 'current'):
                sm.current = 'main'

    def run_test(self, provider_key):
        if not self.settings:
            return

        config = self.settings.get_all()
        provider_config = config.get('providers', {}).get(provider_key, {})
        api_key = provider_config.get('api_key', '')

        if hasattr(self, 'ids'):
            tab_map = {'openai_compat': 'openai_tab', 'deepseek': 'deepseek_tab', 'anthropic': 'anthropic_tab'}
            tab_id = tab_map.get(provider_key)
            if tab_id and tab_id in self.ids:
                tab = self.ids[tab_id]
                if hasattr(tab, 'get_config'):
                    live_config = tab.get_config()
                    api_key = live_config.get('api_key', api_key)

        if not api_key:
            self._show_popup('测试连接', '请先输入API密钥', False)
            return

        test_config = dict(config)
        test_config['providers'] = dict(config.get('providers', {}))
        test_config['providers'][provider_key] = dict(provider_config)
        test_config['providers'][provider_key]['api_key'] = api_key

        if hasattr(self, 'ids'):
            tab_map = {'openai_compat': 'openai_tab', 'deepseek': 'deepseek_tab', 'anthropic': 'anthropic_tab'}
            tab_id = tab_map.get(provider_key)
            if tab_id and tab_id in self.ids:
                tab = self.ids[tab_id]
                if hasattr(tab, 'get_config'):
                    live = tab.get_config()
                    test_config['providers'][provider_key].update(live)

        if hasattr(self, 'ids'):
            tab_id = tab_map.get(provider_key)
            if tab_id and tab_id in self.ids:
                self.ids[tab_id].set_testing(True)

        def _run():
            try:
                client = create_client_by_provider(test_config, provider_key)
                ok, msg = client.validate_connection()
                Clock.schedule_once(lambda dt: self._on_test_result(ok, msg, provider_key))
            except Exception as e:
                Clock.schedule_once(lambda dt: self._on_test_result(False, str(e), provider_key))

        threading.Thread(target=_run, daemon=True).start()

    def _on_test_result(self, ok, msg, provider_key):
        if hasattr(self, 'ids'):
            tab_map = {'openai_compat': 'openai_tab', 'deepseek': 'deepseek_tab', 'anthropic': 'anthropic_tab'}
            tab_id = tab_map.get(provider_key)
            if tab_id and tab_id in self.ids:
                self.ids[tab_id].set_testing(False)

        self._show_popup(
            '连接成功' if ok else '连接失败',
            '连接成功！' if ok else f'连接失败:\n{msg}',
            ok
        )

    def _show_popup(self, title, message, is_success):
        content = Label(text=message, text_size=(self.width * 0.7, None),
                        halign='center', valign='middle')
        popup = Popup(title=title, content=content,
                      size_hint=(0.75, 0.35))
        popup.open()

    def update_theme(self, colors):
        self.bg_color = hex_to_rgba(colors.get('bg_primary', '#F0F2F5'))
        self.text_color = colors.get('text_primary', '#1F2937')
        self.tab_bg = hex_to_rgba(colors.get('bg_card', '#FFFFFF'))
        self.tab_normal_bg = hex_to_rgba(colors.get('border', '#E2E8F0'))
        self.tab_normal_text = colors.get('text_secondary', '#64748B')
        self.save_btn_color = hex_to_rgba(colors.get('bg_button_save', '#3B82F6'))
        self.cancel_btn_color = hex_to_rgba(colors.get('border', '#E5E7EB'))
        self.cancel_text_color = colors.get('text_primary', '#374151')

        is_dark = self.bg_color == hex_to_rgba('#0F172A')
        if hasattr(self, 'ids'):
            for tab_id in ('openai_tab', 'deepseek_tab', 'anthropic_tab'):
                if tab_id in self.ids:
                    self.ids[tab_id].update_theme(colors, is_dark)
