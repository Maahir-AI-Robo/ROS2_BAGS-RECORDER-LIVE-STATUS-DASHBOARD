import sqlite3
import json
import time
from pathlib import Path

class SessionIndex:
    def __init__(self, config):
        self.db_path = Path(config.get('index_db_path', './data/index/index.db'))
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                start_time INTEGER NOT NULL,
                end_time INTEGER,
                total_bytes INTEGER DEFAULT 0,
                total_messages INTEGER DEFAULT 0,
                segment_count INTEGER DEFAULT 0,
                topics TEXT,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS segments (
                segment_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                sequence_number INTEGER NOT NULL,
                byte_size INTEGER NOT NULL,
                checksum_sha256 TEXT NOT NULL,
                file_path TEXT NOT NULL,
                upload_status TEXT DEFAULT 'pending',
                created_at INTEGER NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        conn.commit()
        conn.close()
    
    async def add_session(self, session_id, topics):
        now = int(time.time())
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            INSERT OR REPLACE INTO sessions
            (session_id, status, start_time, topics, created_at, updated_at)
            VALUES (?, 'CREATED', ?, ?, ?, ?)
        ''', (session_id, now, json.dumps(topics), now, now))
        conn.commit()
        conn.close()
    
    async def add_segment(self, segment):
        now = int(time.time())
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            INSERT OR REPLACE INTO segments
            (segment_id, session_id, sequence_number, byte_size, checksum_sha256, file_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            segment['segment_id'], segment['session_id'], segment['sequence_number'],
            segment['byte_size'], segment['checksum_sha256'], segment['file_path'], now
        ))
        conn.commit()
        conn.close()
    
    async def update_session_status(self, session_id, status):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('UPDATE sessions SET status = ?, updated_at = ? WHERE session_id = ?', (status, int(time.time()), session_id))
        conn.commit()
        conn.close()