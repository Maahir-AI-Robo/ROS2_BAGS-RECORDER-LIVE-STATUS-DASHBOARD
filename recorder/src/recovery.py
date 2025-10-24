import os
import json
from pathlib import Path
from datetime import datetime

class RecoveryManager:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        self.recovery_log_path = self.storage_path / '.recovery'
        self.recovery_log_path.mkdir(parents=True, exist_ok=True)
    
    def detect_incomplete_segments(self, session_id):
        session_dir = self.storage_path / session_id
        incomplete = []
        if session_dir.exists():
            for f in session_dir.glob('segment_*.tmp'):
                incomplete.append(str(f))
        return incomplete
    
    def rollback_segment(self, segment_path):
        if os.path.exists(segment_path):
            os.remove(segment_path)
            return True
        return False
    
    def log_recovery_action(self, session_id, action, details):
        log_file = self.recovery_log_path / f'{session_id}_recovery.json'
        record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'action': action,
            'details': details
        }
        history = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                history = json.load(f)
        history.append(record)
        with open(log_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def recover_session(self, session_id):
        incomplete = self.detect_incomplete_segments(session_id)
        for segment in incomplete:
            self.rollback_segment(segment)
            self.log_recovery_action(session_id, 'rollback', {'segment': segment})
        return len(incomplete)
