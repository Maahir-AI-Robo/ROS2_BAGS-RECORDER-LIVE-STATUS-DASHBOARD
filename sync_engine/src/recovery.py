import json
from pathlib import Path

class RecoveryEngine:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        self.recovery_dir = self.storage_path / '.recovery'
        self.recovery_dir.mkdir(parents=True, exist_ok=True)
    
    def save_upload_state(self, job_id, state: dict):
        p = self.recovery_dir / f'{job_id}_state.json'
        p.write_text(json.dumps(state, indent=2))
    
    def load_upload_state(self, job_id):
        p = self.recovery_dir / f'{job_id}_state.json'
        return json.loads(p.read_text()) if p.exists() else None
    
    def get_incomplete_uploads(self):
        out = []
        for p in self.recovery_dir.glob('*_state.json'):
            s = json.loads(p.read_text())
            if s.get('status') in ('queued', 'uploading'):
                out.append(s)
        return out