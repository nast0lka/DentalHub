from app.dao.base import BaseDAO
from app.users.models import User
from app.database import async_session_maker

class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user(cls, user_data: dict) -> User:
        user = cls.model(**user_data)
        
        async with async_session_maker() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user