from fastapi import WebSocket
from typing import Set

class WebSocketBroadcaster:
    def __init__(self):
        self.clients: Set[WebSocket] = set()
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)
    
    async def disconnect(self, ws: WebSocket):
        self.clients.discard(ws)
    
    async def broadcast(self, message: dict):
        dead = []
        for ws in list(self.clients):
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.clients.discard(ws)