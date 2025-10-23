import os
import shutil
from pathlib import Path

class StorageManager:
    def __init__(self, config):
        self.config = config
        self.data_path = Path(config.get('data_path', './data/storage'))
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    async def store_segment(self, session_id: str, segment_id: str, data: bytes):
        session_dir = self.data_path / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        segment_path = session_dir / f'{segment_id}.bin'
        tmp = segment_path.with_suffix(segment_path.suffix + '.tmp')
        with open(tmp, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        tmp.replace(segment_path)
        return str(segment_path)
    
    async def get_segment(self, session_id, segment_id):
        p = self.data_path / session_id / f'{segment_id}.bin'
        if p.exists():
            return p.read_bytes()
        return None
    
    async def list_segments(self, session_id):
        session_dir = self.data_path / session_id
        if not session_dir.exists():
            return []
        return [f.stem for f in session_dir.glob('*.bin')]
    
    async def delete_session(self, session_id):
        session_dir = self.data_path / session_id
        if session_dir.exists():
            shutil.rmtree(session_dir)
            return True
        return False
