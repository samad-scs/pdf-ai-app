from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from .auth import get_user_credentials
from ..core.database import engine, Base
from src.models import *

router = APIRouter()
templates = Jinja2Templates(directory="src/logger_panel/templates")

ADMIN_USER = {"email": "admin@example.com", "password": "1234"}


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
        raise RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("base.html", {"request": request})


@router.post("/db-sync", include_in_schema=False)
async def db_sync():
    print("Starting DB sync...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return JSONResponse(
            {
                "status": "success",
                "message": "Database tables created/synced successfully",
            }
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}
