import logging

from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.staticfiles import StaticFiles

from app.configuration.admin import flask_app
from app.configuration.logging_config import LOGGING_CONFIG
from app.configuration.settings import settings
from app.routes import cinema_room_controller

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()
app.include_router(cinema_room_controller.router)
app.mount("/", WSGIMiddleware(flask_app))
app.mount("/media", StaticFiles(directory="./media"), name="media")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
                host=settings.app_settings.HOST,
                port=settings.app_settings.PORT,
                reload=True)