from fastapi import HTTPException, Request

def get_user_credentials(request: Request):
    user = request.session.get("user")
    return user
    