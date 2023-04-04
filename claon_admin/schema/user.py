from uuid import uuid4

from sqlalchemy import Column, String, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from claon_admin.schema.conn import Base


class User(Base):
    __tablename__ = 'tb_user'
    id = Column(String(length=255), primary_key=True, default=str(uuid4()))
    profile_image = Column(String(length=512))
    nickname = Column(String(length=20))
    email = Column(String(length=64))
    instagram_nickname = Column(String(length=30))
    role = Column(String(length=16))


class UserRepository:
    @staticmethod
    async def find_by_id(session: AsyncSession, user_id: str):
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().one_or_none()

    @staticmethod
    async def exist_by_id(session: AsyncSession, user_id: str):
        result = await session.execute(select(exists().where(User.id == user_id)))
        return result.scalar()

    @staticmethod
    async def save(session: AsyncSession, user: User):
        session.add(user)
        await session.flush()
        return user