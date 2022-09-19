from fastapi import APIRouter
from starlette.websockets import WebSocket

websocket_router = APIRouter()

room = {}

@websocket_router.websocket('/map')
async def join_room(ws: WebSocket):
	try:
		pass

	except Exception as e:
		print(e)
