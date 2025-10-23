import json
import time
import uuid
from pathlib import Path

class UploadQueue:
    def __init__(self, config):
        self.config = config
        self.queue_path = Path(config.get('queue_path', './data/queue/queue.json'))
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        self._queue = self._load()
    
    async def enqueue(self, payload: dict):
        job_id = str(uuid.uuid4())
        payload = dict(payload)
        payload.update({
            'job_id': job_id,
            'status': 'queued',
            'retry_count': 0,
            'created_at': time.time(),
            'updated_at': time.time(),
        })
        self._queue.append(payload)
        self._save()
        return job_id
    
    async def list(self):
        return list(self._queue)
    
    async def update_status(self, job_id: str, status: str):
        for job in self._queue:
            if job['job_id'] == job_id:
                job['status'] = status
                job['updated_at'] = time.time()
                self._save()
                return True
        return False
    
    def _load(self):
        if self.queue_path.exists():
            return json.loads(self.queue_path.read_text())
        return []
    
    def _save(self):
        self.queue_path.write_text(json.dumps(self._queue, indent=2))
