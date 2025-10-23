import os
import hashlib
import json
import uuid
import time

class SegmentWriter:
    def __init__(self, config):
        self.config = config
        self.storage_path = config.get('local_path', './data')
        self.compression = config.get('compression', 'none')
        os.makedirs(self.storage_path, exist_ok=True)
        
    def write_segment(self, session_id, sequence, messages):
        segment_id = str(uuid.uuid4())
        
        # Create session directory
        session_dir = os.path.join(self.storage_path, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # Serialize messages
        data = json.dumps(messages).encode('utf-8')
        
        # Compress if needed
        if self.compression == 'zstd':
            try:
                import zstandard as zstd
                cctx = zstd.ZstdCompressor(level=3)
                data = cctx.compress(data)
            except Exception:
                pass
        
        # Calculate checksum
        checksum = hashlib.sha256(data).hexdigest()
        
        # Write segment atomically
        file_path = os.path.join(session_dir, f'segment_{sequence:06d}.bin')
        temp_path = file_path + '.tmp'
        
        with open(temp_path, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        
        os.rename(temp_path, file_path)
        
        message_count = sum(len(v) if isinstance(v, list) else 1 for v in messages.values())
        
        return {
            'segment_id': segment_id,
            'session_id': session_id,
            'sequence_number': sequence,
            'byte_size': len(data),
            'checksum_sha256': checksum,
            'file_path': file_path,
            'message_count': message_count,
            'start_timestamp_ns': int(time.time_ns()),
            'end_timestamp_ns': int(time.time_ns()),
            'topics': list(messages.keys())
        }