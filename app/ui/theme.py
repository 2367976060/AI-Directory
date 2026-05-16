"""Kivy color constants for light/dark themes. All colors as hex strings."""


def hex_to_rgba(hex_color):
    """Convert hex color (#RGB or #RRGGBB) to Kivy-compatible (r, g, b, a) float tuple."""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, 1.0)


LIGHT_COLORS = {
    'bg_primary': '#F0F2F5',
    'bg_card': '#FFFFFF',
    'bg_input': '#FAFBFC',
    'bg_header': '#1E293B',
    'bg_log': '#0F172A',
    'bg_sidebar': '#FFFFFF',
    'bg_nav': '#FFFFFF',
    'bg_button_start': '#059669',
    'bg_button_stop': '#DC2626',
    'bg_button_clear': '#6B7280',
    'bg_button_open': '#3B82F6',
    'bg_button_test': '#10B981',
    'bg_button_save': '#3B82F6',
    'bg_tab_selected': '#3B82F6',
    'text_primary': '#1F2937',
    'text_secondary': '#64748B',
    'text_log_info': '#CBD5E1',
    'text_log_success': '#27AE60',
    'text_log_warn': '#F39C12',
    'text_log_error': '#E74C3C',
    'text_muted': '#9CA3AF',
    'text_button': '#FFFFFF',
    'text_on_primary': '#FFFFFF',
    'border': '#E2E8F0',
    'border_focus': '#3B82F6',
    'accent_blue': '#3B82F6',
    'accent_green': '#10B981',
    'accent_red': '#EF4444',
    'accent_amber': '#F59E0B',
    'step_pending': '#94A3B8',
    'step_running': '#3B82F6',
    'step_done': '#10B981',
    'step_error': '#EF4444',
    'step_bg_pending': 'transparent',
    'step_bg_running': '#EFF6FF',
    'step_bg_done': '#ECFDF5',
    'step_bg_error': '#FEF2F2',
    'progress_global': '#3B82F6',
    'progress_step': '#10B981',
    'scrollbar': '#CBD5E1',
}

DARK_COLORS = {
    'bg_primary': '#0F172A',
    'bg_card': '#1E293B',
    'bg_input': '#0F172A',
    'bg_header': '#0B1120',
    'bg_log': '#020617',
    'bg_sidebar': '#0F172A',
    'bg_nav': '#1E293B',
    'bg_button_start': '#059669',
    'bg_button_stop': '#DC2626',
    'bg_button_clear': '#475569',
    'bg_button_open': '#6366F1',
    'bg_button_test': '#10B981',
    'bg_button_save': '#6366F1',
    'bg_tab_selected': '#6366F1',
    'text_primary': '#E2E8F0',
    'text_secondary': '#94A3B8',
    'text_log_info': '#94A3B8',
    'text_log_success': '#27AE60',
    'text_log_warn': '#F39C12',
    'text_log_error': '#E74C3C',
    'text_muted': '#64748B',
    'text_button': '#FFFFFF',
    'text_on_primary': '#FFFFFF',
    'border': '#1E293B',
    'border_focus': '#6366F1',
    'accent_blue': '#6366F1',
    'accent_green': '#10B981',
    'accent_red': '#EF4444',
    'accent_amber': '#F59E0B',
    'step_pending': '#64748B',
    'step_running': '#6366F1',
    'step_done': '#10B981',
    'step_error': '#EF4444',
    'step_bg_pending': 'transparent',
    'step_bg_running': '#1E293B',
    'step_bg_done': '#0F172A',
    'step_bg_error': '#1E293B',
    'progress_global': '#6366F1',
    'progress_step': '#10B981',
    'scrollbar': '#475569',
}

ICONS = {
    'pending': '○',
    'running': '→',
    'done': '●',
    'error': '▲',
}

STEP_NAMES = [
    '需求智能解析整理',
    '整体项目架构规划设计',
    '功能模块拆分与结构搭建',
    '前后端完整源码智能生成',
    '统一接口文档自动编写',
    '代码自检优化与错误排查',
    '全项目自动整理打包输出',
]

STEP_DETAILS = [
    '分析需求，生成需求文档',
    '规划技术栈与架构方案',
    '拆分模块，搭建目录结构',
    '生成完整项目源代码',
    '编写API接口文档',
    '代码审查与质量优化',
    '打包压缩最终项目文件',
]


class ThemeManager:
    def __init__(self):
        self._current_theme = 'light'

    @property
    def colors(self):
        return LIGHT_COLORS if self._current_theme == 'light' else DARK_COLORS

    @property
    def is_dark(self):
        return self._current_theme == 'dark'

    def toggle(self):
        self._current_theme = 'dark' if self._current_theme == 'light' else 'light'
        return self._current_theme

    def set_theme(self, theme_name):
        if theme_name in ('light', 'dark'):
            self._current_theme = theme_name

    def get_step_icon(self, status):
        return ICONS.get(status, '○')

    def get_step_color(self, status):
        return self.colors.get(f'step_{status}', '#94A3B8')

    def get_step_bg(self, status):
        return self.colors.get(f'step_bg_{status}', 'transparent')
