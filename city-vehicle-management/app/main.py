from fastapi import FastAPI
from app.routers import users
from app.routers import vehicle_records
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.crud.archive import archive_old_partitions
from app.config.db_conf import AsyncMasterSessionLocal
import logging
import os
from logging.handlers import RotatingFileHandler

# 确定日志目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 配置根日志器
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 文件处理器（自动轮转，每个文件最大10MB，保留5个备份）
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    maxBytes=10*1024*1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)

# 错误级别单独文件
error_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "error.log"),
    maxBytes=10*1024*1024,
    backupCount=5,
    encoding="utf-8"
)
error_handler.setFormatter(log_format)
error_handler.setLevel(logging.ERROR)

# 控制台处理器（开发时可选）
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)

# 获取 root logger 并添加处理器
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(error_handler)
if os.getenv("ENV") != "production":  # 开发环境加控制台
    logger.addHandler(console_handler)


# 定义 lifespan 管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_archive, 'cron', day=1, hour=2)
    scheduler.start()
    yield
    # 关闭时执行（可选，用于清理）
    scheduler.shutdown()

# 创建唯一的 app 实例，并传入 lifespan
app = FastAPI(lifespan=lifespan)

# 静态文件目录
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],     # 允许的请求方法
    allow_headers=["*"],     # 允许的请求头
)

# 网站图标
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/")
async def root():
    return {"message": "欢迎来到城市车辆管理系统 API"}

# 挂载路由
app.include_router(users.router)
app.include_router(vehicle_records.router)

# 定时任务要执行的异步函数
async def scheduled_archive():
    async with AsyncMasterSessionLocal() as db:
        await archive_old_partitions(db)