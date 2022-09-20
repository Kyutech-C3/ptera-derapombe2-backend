from fastapi import APIRouter
from starlette.websockets import WebSocket

websocket_router = APIRouter()

clients = {}

@websocket_router.websocket('/map')
async def join_room(ws: WebSocket):
	await ws.accept()
	key = ws.headers.get('sec-websocket-key')
	clients[key] = ws
	try:
		while True:
			pass
	except Exception:
		await ws.close()
		del clients[key]
