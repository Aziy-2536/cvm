from fastapi import FastAPI
from app.routers import users
from app.routers import vehicle_records
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# 注册异常处理器

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],     # 允许的请求方法
    allow_headers=["*"],     # 允许的请求头
)

#网站图标
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/")
async def root():
    return {"message": "欢迎来到城市车辆管理系统 API"}

# 挂载路由/注册路由
app.include_router(users.router)
app.include_router(vehicle_records.router)
