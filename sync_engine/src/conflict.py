class ConflictResolver:
    def __init__(self):
        self.conflicts = []
    
    def detect_conflict(self, local_manifest, remote_manifest):
        return local_manifest.get('segment_count') != remote_manifest.get('segment_count')
    
    def resolve_conflict(self, local_manifest, remote_manifest, strategy='local_wins'):
        if strategy == 'local_wins':
            return local_manifest
        if strategy == 'remote_wins':
            return remote_manifest
        if strategy == 'merge':
            merged = local_manifest.copy()
            merged['segments'] = sorted(list(set(local_manifest.get('segments', []) + remote_manifest.get('segments', []))))
            return merged
        return local_manifest