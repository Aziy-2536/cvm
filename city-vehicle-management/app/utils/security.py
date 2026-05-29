# # app/utils/security.py
# from passlib.context import CryptContext
# from jose import jwt
# from datetime import datetime, timedelta
# from app.config import settings

# # 使用 Argon2，无长度限制
# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# from passlib.context import CryptContext
# from passlib.hash import argon2

# pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_hash_password(password):
#     return pwd_context.hash(password)  
# from passlib.context import CryptContext

# # 将 schemes 改为 ["argon2"]，并设置默认使用 argon2
# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# def get_hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# app/utils/security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 为了兼容现有代码，添加别名
hash_password = get_hash_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)