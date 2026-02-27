from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse

from app.tasks.tasks import send_confirmation_email
from app.users.auth import (authenticate_user, get_current_user,
                            get_password_hash)
from app.users.dao import UserDAO
from app.users.models import User
from app.users.schemas import SUserAuth, UserBase
from app.users.token import (create_access_token, create_refresh_token,
                             decode_token)

router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router_auth.post("/register")
async def register_user(user_data: UserBase = Depends(UserBase.as_form)):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise Exception("User with this email already exists")
    password_hash = get_password_hash(user_data.password)
    await UserDAO.add(
        name=user_data.name,
        lastname=user_data.lastname,
        age=user_data.age,
        email=user_data.email,
        password_hash=password_hash
    )
    user = await UserDAO.find_one_or_none(email=user_data.email)
    send_confirmation_email.delay(user.id)
    resp = RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER
    )
    resp.set_cookie("registration_sent", "1", max_age=60, httponly=True)
    return resp

@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth = Depends(SUserAuth.as_form)):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise Exception("Invalid email or password")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    response = RedirectResponse( 
        url="/", 
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True, max_age=7*24*3600)
    return response

@router_auth.get("/logout")
async def logout_user(response: Response):
    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router_auth.post("/refresh")
async def refresh_token(response: Response, request: Request):
    token = request.cookies.get("refresh_token")

    def clear_and_redirect():
        r = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        r.delete_cookie("access_token")
        r.delete_cookie("refresh_token")
        return r

    if not token:
        return clear_and_redirect()
    
    try:
        payload = decode_token(token, expected_type="refresh")
        user_id: str = payload.get("sub")
        if not user_id:
            return clear_and_redirect()
    except Exception:
        return clear_and_redirect()

    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        return clear_and_redirect()

    access_token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("access_token", access_token, httponly=True)
    return response


@router_auth.get("/confirm")
async def confirm_email(token: str):
    try:
        payload = decode_token(token, expected_type="access")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise Exception("Invalid token")
    except Exception:
        raise Exception("Invalid or expired token")

    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise Exception("User not found")

    if user.is_verified:
        return RedirectResponse(url="/login")

    await UserDAO.update(user_id=int(user_id), is_verified=True)

    return RedirectResponse(url="/login")


@router_auth.get("/resend-confirmation")
async def resending_confirmation_email(user: User = Depends(get_current_user)):
    send_confirmation_email.delay(user.id)
    return RedirectResponse(url="/profile")