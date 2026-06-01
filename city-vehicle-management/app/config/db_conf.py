import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== 主库配置 (写操作) ======================
MASTER_DB_URL = f"mysql+asyncmy://{os.getenv('MYSQL_MASTER_USER')}:{os.getenv('MYSQL_MASTER_PASSWORD')}@{os.getenv('MYSQL_MASTER_HOST')}:{os.getenv('MYSQL_MASTER_PORT')}/{os.getenv('MYSQL_MASTER_DATABASE')}?charset=utf8mb4"

# ====================== 从库配置 (读操作) ======================
SLAVE_DB_URL = f"mysql+asyncmy://{os.getenv('MYSQL_SLAVE_USER')}:{os.getenv('MYSQL_SLAVE_PASSWORD')}@{os.getenv('MYSQL_SLAVE_HOST')}:{os.getenv('MYSQL_SLAVE_PORT')}/{os.getenv('MYSQL_SLAVE_DATABASE')}?charset=utf8mb4"

# 创建引擎
master_engine = create_async_engine(
    MASTER_DB_URL,
    pool_size=8,           # 根据实际情况调整
    max_overflow=15,
    pool_pre_ping=True,    # 防止连接断开
    echo=False             # 生产环境关闭，调试时可改为 True
)

slave_engine = create_async_engine(
    SLAVE_DB_URL,
    pool_size=12,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False
)

# 创建会话工厂
AsyncMasterSessionLocal = sessionmaker(
    master_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

AsyncSlaveSessionLocal = sessionmaker(
    slave_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# ====================== 依赖注入函数 ======================
async def get_master_session():
    """用于写操作"""
    async with AsyncMasterSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_slave_session():
    """用于读操作"""
    async with AsyncSlaveSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_master_read_session():   # 专门给登录、刚写入后立即读取等场景用
    async with AsyncMasterSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            
# import os
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.config.db_conf import AsyncMasterSessionLocal, AsyncSlaveSessionLocal

# load_dotenv()

# # 主库连接字符串
# MASTER_DB_URL = f"mysql+asyncmy://{os.getenv('MYSQL_MASTER_USER')}:{os.getenv('MYSQL_MASTER_PASSWORD')}@{os.getenv('MYSQL_MASTER_HOST')}:{os.getenv('MYSQL_MASTER_PORT')}/{os.getenv('MYSQL_MASTER_DATABASE')}?charset=utf8mb4"

# # 从库连接字符串
# SLAVE_DB_URL = f"mysql+asyncmy://{os.getenv('MYSQL_SLAVE_USER')}:{os.getenv('MYSQL_SLAVE_PASSWORD')}@{os.getenv('MYSQL_SLAVE_HOST')}:{os.getenv('MYSQL_SLAVE_PORT')}/{os.getenv('MYSQL_SLAVE_DATABASE')}?charset=utf8mb4"

# master_engine = create_async_engine(MASTER_DB_URL, pool_size=10, max_overflow=20)
# slave_engine = create_async_engine(SLAVE_DB_URL, pool_size=20, max_overflow=40)

# AsyncMasterSessionLocal = sessionmaker(master_engine, class_=AsyncSession, expire_on_commit=False)
# AsyncSlaveSessionLocal = sessionmaker(slave_engine, class_=AsyncSession, expire_on_commit=False)

# async def get_master_db() -> AsyncSession:
#     """提供主库会话（用于写操作）"""
#     async with AsyncMasterSessionLocal() as session:
#         yield session

# async def get_slave_db() -> AsyncSession:
#     """提供从库会话（用于读操作）"""
#     async with AsyncSlaveSessionLocal() as session:
#         yield session

# import os
# from dotenv import load_dotenv
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession

# load_dotenv()

# # 主库连接字符串
# MASTER_DB_URL = f"mysql+asyncmy://{os.getenv('MYSQL_MASTER_USER')}:{os.getenv('MYSQL_MASTER_PASSWORD')}@{os.getenv('MYSQL_MASTER_HOST')}:{os.getenv('MYSQL_MASTER_PORT')}/{os.getenv('MYSQL_MASTER_DATABASE')}?charset=utf8mb4"

# # 从库连接字符串
# SLAVE_DB_URL = f"mysql+asyncmy://{os.getenv('MYSQL_SLAVE_USER')}:{os.getenv('MYSQL_SLAVE_PASSWORD')}@{os.getenv('MYSQL_SLAVE_HOST')}:{os.getenv('MYSQL_SLAVE_PORT')}/{os.getenv('MYSQL_SLAVE_DATABASE')}?charset=utf8mb4"

# master_engine = create_async_engine(MASTER_DB_URL, pool_size=10, max_overflow=20)
# slave_engine = create_async_engine(SLAVE_DB_URL, pool_size=20, max_overflow=40)

# AsyncMasterSessionLocal = sessionmaker(master_engine, class_=AsyncSession, expire_on_commit=False)
# AsyncSlaveSessionLocal = sessionmaker(slave_engine, class_=AsyncSession, expire_on_commit=False)

