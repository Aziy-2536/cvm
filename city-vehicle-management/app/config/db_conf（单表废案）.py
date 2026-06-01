from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine
from sqlalchemy.engine.url import URL
import os
from dotenv import load_dotenv

load_dotenv()

ASYNC_DATABASE_URL = URL.create(
    drivername="mysql+aiomysql",  # 使用异步驱动
    username="root",          # 例如: root
    password=os.getenv("MYSQL_PASSWORD", ""),            # 即使包含 @ 等特殊字符也无须手动转义
    host="localhost",              # 或 127.0.0.1
    port=3306,                     # MySQL 默认端口
    database="city_vehicle_db"         # 例如: fastapi_db
)

engine = create_async_engine(ASYNC_DATABASE_URL, 
                             echo=True,
                             pool_size=10,
                             max_overflow=20
                             )

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False   # 防止提交后过期
)

# 依赖注入：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # 回滚未提交的事务，确保连接池健康
        except Exception :
            await session.rollback()  # 出现异常时回滚事务
            raise
        finally:
            await session.close()     # 确保会话被正确关闭，释放连接回池
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()   # 只有正常结束才提交
        except Exception:
            await session.rollback()
            raise
        # 不需要 finally 手动 close，async with 退出时会自动关闭