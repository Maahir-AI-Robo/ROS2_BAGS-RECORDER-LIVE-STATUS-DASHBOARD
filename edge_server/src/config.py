import json
import yaml
import os

class EdgeServerConfig:
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
    
    def get_server_config(self):
        return self.config.get('edge_server', {}).get('server', {})
    
    def get_storage_config(self):
        return self.config.get('edge_server', {}).get('storage', {})
    
    def get_queue_config(self):
        return self.config.get('edge_server', {}).get('queue', {})
    
    def get_cloud_config(self):
        return self.config.get('edge_server', {}).get('cloud', {})
