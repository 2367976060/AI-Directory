import os
import json
import shutil
from pathlib import Path


def _get_config_dir():
    try:
        import sys
        if sys.platform == 'android':
            try:
                from android.storage import app_storage_path
                return Path(app_storage_path()) / 'AIProjectGenerator'
            except ImportError:
                return Path(os.path.expanduser('~')) / '.AIProjectGenerator'
        else:
            if os.name == 'nt':
                return Path(os.path.expandvars('%APPDATA%')) / 'AIProjectGenerator'
            return Path(os.path.expanduser('~')) / '.AIProjectGenerator'
    except Exception:
        return Path(os.path.expanduser('~')) / '.AIProjectGenerator'


class SettingsManager:
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
        self._config_dir = _get_config_dir()
        self._config_file = self._config_dir / 'config.json'
        self._backup_file = self._config_dir / 'config.backup.json'
        self._defaults = self._load_defaults()
        self._config = {}
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        self._config_dir.mkdir(parents=True, exist_ok=True)

    def _load_defaults(self):
        defaults_path = Path(__file__).parent / 'defaults.json'
        with open(defaults_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load(self):
        if self._config_file.exists():
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                self._merge_defaults()
            except (json.JSONDecodeError, IOError):
                self._try_restore_backup()
        else:
            self._config = dict(self._defaults)
            self.save()

    def _merge_defaults(self):
        for key, value in self._defaults.items():
            if key not in self._config:
                self._config[key] = value
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key not in self._config[key]:
                        self._config[key][sub_key] = value[sub_key]
                    elif isinstance(sub_value, dict):
                        for k, v in sub_value.items():
                            if k not in self._config[key][sub_key]:
                                self._config[key][sub_key][k] = v

    def _try_restore_backup(self):
        if self._backup_file.exists():
            try:
                with open(self._backup_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                self.save()
            except (json.JSONDecodeError, IOError):
                self._config = dict(self._defaults)
                self.save()
        else:
            self._config = dict(self._defaults)
            self.save()

    def save(self):
        try:
            if self._config_file.exists():
                shutil.copy2(self._config_file, self._backup_file)
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise RuntimeError(f"保存配置失败: {e}")

    def get(self, key, default=None):
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key, value):
        keys = key.split('.')
        target = self._config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def get_all(self):
        return dict(self._config)

    def get_provider_config(self, provider_name=None):
        provider = provider_name or self.get('current_provider', 'openai_compat')
        return self.get(f'providers.{provider}', {})

    def set_provider_config(self, provider, config_dict):
        self._config.setdefault('providers', {})
        self._config['providers'][provider] = config_dict

    @property
    def app_data_dir(self):
        return self._config_dir

    @property
    def projects_dir(self):
        output = self.get('output_dir', '')
        if output:
            return Path(output)
        return self._config_dir / 'projects'
