import time
from datetime import datetime

class TelemetryEmitter:
    def __init__(self, config):
        self.config = config
        self.metrics = {}
        self.logs = []
    
    def emit_metric(self, topic, message_rate_hz, byte_rate_mbps, buffer_occupancy_percent, dropped_messages):
        metric = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'topic': topic,
            'message_rate_hz': message_rate_hz,
            'byte_rate_mbps': byte_rate_mbps,
            'buffer_occupancy_percent': buffer_occupancy_percent,
            'dropped_messages': dropped_messages
        }
        self.metrics[topic] = metric
        return metric
    
    def emit_alert(self, severity, category, message, session_id=None, topic=None):
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'severity': severity,
            'category': category,
            'message': message,
            'session_id': session_id,
            'topic': topic
        }
    
    def emit_log(self, level, component, message, session_id=None):
        log = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'component': component,
            'message': message,
            'session_id': session_id
        }
        self.logs.append(log)
        return log
    
    def get_metrics(self):
        return self.metrics
    
    def get_logs(self):
        return self.logs

