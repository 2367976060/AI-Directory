"""Observer-pattern event bus replacement for QObject/Signal."""


class SignalBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._callbacks = {}

    def on(self, event_name, callback):
        self._callbacks.setdefault(event_name, []).append(callback)

    def off(self, event_name, callback):
        callbacks = self._callbacks.get(event_name, [])
        if callback in callbacks:
            callbacks.remove(callback)

    def emit(self, event_name, *args, **kwargs):
        for cb in self._callbacks.get(event_name, []):
            cb(*args, **kwargs)

    def clear(self):
        self._callbacks.clear()

    # Convenience emitters matching desktop signal names
    def start_requested(self, input_text, config):
        self.emit('start_requested', input_text, config)

    def cancel_requested(self):
        self.emit('cancel_requested')

    def log_message(self, level, message):
        self.emit('workflow_log', level, message)

    def step_changed(self, index, status):
        self.emit('workflow_step_changed', index, status)

    def progress_updated(self, step_index, percent, message):
        self.emit('workflow_progress', step_index, percent, message)

    def global_progress(self, percent):
        self.emit('update_global_progress', percent)

    def workflow_started(self):
        self.emit('workflow_started')

    def workflow_completed(self, success, output_path):
        self.emit('workflow_completed', success, output_path)

    def workflow_error(self, step_index, error_msg):
        self.emit('workflow_error', step_index, error_msg)

    def settings_changed(self, config):
        self.emit('settings_changed', config)
