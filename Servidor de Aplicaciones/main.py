from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api._init_ import router as message_router
from database import Base, engine

def get_application():

    app = FastAPI(title="Proyecto 2 Distribuidos", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(message_router, prefix="/MOB/api")
    return app

app = get_application()