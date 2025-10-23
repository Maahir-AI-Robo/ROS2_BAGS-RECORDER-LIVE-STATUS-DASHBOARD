import time

class MetricsCollector:
    def __init__(self):
        self.start = time.time()
        self.sessions = {}
    
    def record_upload(self, session_id, segment_id, bytes_uploaded, duration):
        s = self.sessions.setdefault(session_id, {'uploads': [], 'total_bytes': 0, 'total_duration': 0.0})
        s['uploads'].append({
            'segment_id': segment_id,
            'bytes': bytes_uploaded,
            'duration': duration,
            'rate_mbps': (bytes_uploaded / 1024 / 1024) / duration if duration > 0 else 0.0
        })
        s['total_bytes'] += bytes_uploaded
        s['total_duration'] += duration
    
    def get_metrics(self, session_id=None):
        if session_id:
            return self.sessions.get(session_id, {})
        return self.sessions
    
    def uptime(self):
        return time.time() - self.start