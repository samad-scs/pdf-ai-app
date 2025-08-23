from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.core.response import BaseResponse, success_response
from src.logger_panel.routes import router as logger_router
from src.api.v1 import router as api_v1_router
from src.api.health import router as health_router

from datetime import datetime

app = FastAPI()


# Serve static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-session-key",  # change this to a strong key
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router)
app.include_router(logger_router)
app.include_router(api_v1_router, prefix="/api")
