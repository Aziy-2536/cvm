from fastapi import APIRouter
from app.schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from app.crud import users
from app.config.db_conf import get_master_read_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.utils.response import success_response
from app.schemas.users import UserRegisterRequest, UserRegisterResponse
from app.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register",response_model=UserRegisterResponse, 
             status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterRequest,
                         db: AsyncSession = Depends(get_master_read_session)):
    # 检查用户是否已存在
    if await users.get_user_by_phone(db, user_data.phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该手机号已被注册")
    # 创建新用户
    new_user = await users.create_user(db, user_data)
    return new_user

@router.post("/login", response_model=UserAuthResponse)
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_master_read_session)):
    result = await users.get_user_by_username_or_phone(db, user_data.username)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="用户名或手机号不存在")
    user = result
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    access_token = create_access_token(data={"user_id": user.id, "role_level": user.role_level})
    return UserAuthResponse(access_token=access_token, user_id=user.id, role_level=user.role_level)