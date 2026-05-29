from fastapi import APIRouter
from app.schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from app.crud import users
from app.config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.utils.response import success_response
from app.schemas.users import UserRegisterRequest, UserRegisterResponse

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register",response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    # 检查用户是否已存在
    if await users.get_user_by_phone(db, user_data.phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该手机号已被注册")
    # 创建新用户
    new_user = await users.create_user(db, user_data)
    return new_user

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在 -> 验证密码 -> 生成 Token  → 响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功啦", data=response_data)