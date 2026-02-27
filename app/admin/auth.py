from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.users.auth import (authenticate_user, get_user_from_session)
from app.users.token import create_access_token, create_refresh_token


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await authenticate_user(email, password)

        if user:
            access_token = create_access_token({"sub": str(user.id)})
            refresh_token = create_refresh_token({"sub": str(user.id)})
            request.session.update({"token": access_token, "refresh_token": refresh_token})
            return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse("/admin/login", status_code=303)

        user = await get_user_from_session(request)
        if not user or not user.is_admin:
            return RedirectResponse("/admin/login", status_code=303)

        return True


authentication_backend = AdminAuth(secret_key="...")
