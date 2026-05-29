from fastapi import APIRouter
from app.schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from app.models import users
from app.models import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.utils.response import success_response


router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register_user():
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在 -> 验证密码 -> 生成 Token  → 响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功啦", data=response_data)