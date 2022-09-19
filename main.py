from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from db.models import Base
from routers.main import graphql_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def health():
    return {'health': 'OK'}

app.include_router(graphql_router)
