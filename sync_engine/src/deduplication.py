import hashlib

class Deduplication:
    def __init__(self):
        self.segment_hashes = {}
    
    def add_segment(self, segment_id, data: bytes):
        self.segment_hashes[segment_id] = hashlib.sha256(data).hexdigest()
    
    def is_duplicate(self, data: bytes):
        h = hashlib.sha256(data).hexdigest()
        return h in self.segment_hashes.values()
    
    def get_duplicate_id(self, data: bytes):
        h = hashlib.sha256(data).hexdigest()
        for sid, shash in self.segment_hashes.items():
            if shash == h:
                return sid
        return None