from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER


from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SUserAuth, UserBase

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
    return RedirectResponse(
        url="/login",
        status_code=HTTP_303_SEE_OTHER
    )

@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth = Depends(SUserAuth.as_form)):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise Exception("Invalid email or password")
    access_token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse( 
        url="/", 
        status_code=HTTP_303_SEE_OTHER
    )
    response.set_cookie("access_token", access_token, httponly=True)
    return response

@router_auth.get("/logout")
async def logout_user(response: Response):
    response = RedirectResponse(
        url="/",
        status_code=HTTP_303_SEE_OTHER
    )
    response.delete_cookie("access_token")
    return response