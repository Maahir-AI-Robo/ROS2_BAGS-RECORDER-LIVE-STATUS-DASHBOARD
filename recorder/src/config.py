import os
import json
import yaml

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        if os.path.exists(self.config_file):
            if self.config_file.endswith(('.yaml', '.yml')):
                with open(self.config_file, 'r') as f:
                    return yaml.safe_load(f) or {}
            else:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        return {}
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self._save_config()
    
    def _save_config(self):
        with open(self.config_file, 'w') as f:
            if self.config_file.endswith(('.yaml', '.yml')):
                yaml.dump(self.config, f, default_flow_style=False)
            else:
                json.dump(self.config, f, indent=2)