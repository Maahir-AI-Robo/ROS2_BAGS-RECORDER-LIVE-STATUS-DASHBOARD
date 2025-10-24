import asyncio
import time

class SyncEngine:
    def __init__(self, config, uploader):
        self.config = config
        self.uploader = uploader
        self.jobs = {}
        self.is_running = False
    
    async def start(self):
        self.is_running = True
    
    async def stop(self):
        self.is_running = False
    
    async def queue_upload(self, session_id, segment_id, file_path, checksum):
        job_id = f"{session_id}_{segment_id}_{int(time.time())}"
        self.jobs[job_id] = {
            'job_id': job_id,
            'session_id': session_id,
            'segment_id': segment_id,
            'file_path': file_path,
            'checksum': checksum,
            'status': 'queued',
            'retry_count': 0,
            'created_at': time.time()
        }
        return job_id
    
    async def process_queue(self):
        for job in list(self.jobs.values()):
            if job['status'] == 'queued':
                job['status'] = 'uploading'
                # placeholder: simulate upload
                await asyncio.sleep(0.5)
                job['status'] = 'completed'
    
    async def job_status(self, job_id):
        return self.jobs.get(job_id)