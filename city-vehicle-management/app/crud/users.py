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