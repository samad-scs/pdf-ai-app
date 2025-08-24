from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from .auth import get_user_credentials
from ..core.database import engine, Base
from src.models import *
from alembic import command
from alembic.config import Config
import os
from src.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="src/logger_panel/templates")

ADMIN_USER = {"email": "admin@example.com", "password": "1234"}


# Alembic configuration
ALEMBIC_INI_PATH = "alembic.ini"
ALEMBIC_MIGRATIONS_PATH = "alembic"  # Directory where migration scripts are stored


@router.get("/", include_in_schema=False)
def login_page(request: Request):
    user = get_user_credentials(request)
    if user:
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", include_in_schema=False)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if email == ADMIN_USER["email"] and password == ADMIN_USER["password"]:
        request.session["user"] = {"email": email}
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid credentials"}
    )


@router.get("/logout", include_in_schema=False)
def logout(request: Request):
    print("Logging out user")
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)


@router.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def logger_dashboard(request: Request):
    user = get_user_credentials(request)
    if user is None:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("base.html", {"request": request})


@router.post("/db-sync", include_in_schema=False)
async def db_sync():
    print("Starting DB sync with migrations...")
    try:
        # Initialize Alembic configuration
        alembic_cfg = Config(ALEMBIC_INI_PATH)
        alembic_cfg.set_main_option("script_location", ALEMBIC_MIGRATIONS_PATH)
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

        # Generate migration scripts for model changes
        command.revision(
            alembic_cfg, autogenerate=True, message="Auto-generated migration"
        )

        # Apply migrations to update the database
        command.upgrade(alembic_cfg, "head")

        # Ensure tables are created (for initial setup or non-migrated tables)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        return JSONResponse(
            {
                "status": "success",
                "message": "Database tables created and synced successfully",
            }
        )
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": f"Error during DB sync: {str(e)}"},
            status_code=500,
        )
