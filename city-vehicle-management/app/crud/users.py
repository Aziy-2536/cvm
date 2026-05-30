from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.schemas.users import UserRegisterRequest
from app.utils.security import hash_password
from datetime import datetime
from app.utils.generator import generate_employee_id

# 异步版本：根据手机号查询用户
async def get_user_by_phone(db: AsyncSession, phone: str):
    result = await db.execute(
        select(User).where(User.phone == phone)
    )
    return result.scalar_one_or_none()

# 异步版本：创建用户
async def create_user(db: AsyncSession, user: UserRegisterRequest):
    db_user = User(
        username=user.username,
        phone=user.phone,
        password_hash=hash_password(user.password),
        employee_id=generate_employee_id(),
        role_level=0,
        hire_date=datetime.today()
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_username_or_phone(db: AsyncSession, username: str, phone: str = None):
    """
    根据用户名或手机号查询用户
    如果 phone 未提供，则只使用 username 查询（实际登录时 username 和 phone 可能是同一输入）
    """
    result = await db.execute(
        select(User).where(
            (User.username == username) | (User.phone == username)  # 假设前端传入的 username 可能是手机号
        )
    )
    return result.scalar_one_or_none()