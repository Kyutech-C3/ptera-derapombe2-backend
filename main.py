from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cruds.init import init_base_sign, init_item
from db.database import engine
from db.models import Base
from routers.graphql import graphql_router
from routers.websocket import websocket_router
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./assets/image/X100-2/"), name="static")

init_base_sign()
init_item()

@app.get('/')
async def health():
    return {'health': 'OK'}

app.include_router(graphql_router, prefix='/graphql')
app.include_router(websocket_router, prefix='/ws')
