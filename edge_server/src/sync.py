import asyncio
import os
import time
from pathlib import Path
from .index import SessionIndex
from .queue import UploadQueue

class EdgeSyncService:
    def __init__(self, storage_dir: str, queue_config: dict, index_config: dict, uploader):
        self.storage_dir = Path(storage_dir)
        self.queue = UploadQueue(queue_config)
        self.index = SessionIndex(index_config)
        self.uploader = uploader
        self._running = False
    
    async def start(self):
        self._running = True
    
    async def stop(self):
        self._running = False
    
    async def enqueue_segment(self, segment_meta: dict):
        return await self.queue.enqueue(segment_meta)
    
    async def run_once(self):
        jobs = await self.queue.list()
        for job in jobs:
            if job['status'] != 'queued':
                continue
            await self.queue.update_status(job['job_id'], 'uploading')
            file_path = job.get('file_path')
            if not file_path or not os.path.exists(file_path):
                await self.queue.update_status(job['job_id'], 'failed')
                continue
            start = time.time()
            result = await self.uploader.upload(
                segment_id=job['segment_id'],
                file_path=file_path,
                session_id=job['session_id'],
                checksum=job.get('checksum_sha256', '')
            )
            if result.get('success'):
                await self.queue.update_status(job['job_id'], 'completed')
            else:
                await self.queue.update_status(job['job_id'], 'failed')
    
    async def run_forever(self, interval_sec: int = 2):
        await self.start()
        try:
            while self._running:
                await self.run_once()
                await asyncio.sleep(interval_sec)
        finally:
            await self.stop()