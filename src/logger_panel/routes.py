from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
 
router = APIRouter()
templates = Jinja2Templates(directory="src/logger_panel/templates")

ADMIN_USER = {"email": "admin@example.com", "password": "1234"}

@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if email == ADMIN_USER["email"] and password == ADMIN_USER["password"]:
        request.session["user"] = {"email": email}
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)

@router.get("/admin", response_class=HTMLResponse)
async def logger_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
