# app/config/__init__.py
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    SECRET_KEY: str = "cWmCy5W-kvddV-U5VOipNmKGnt-bIZ8EyRgDNLI8UXo"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    mysql_password: str

    mysql_master_host: str = "localhost"
    mysql_master_port: int = 3306
    mysql_master_user: str = "root"
    mysql_master_password: str = ""
    mysql_master_database: str = "city_vehicle_db"
    
    # 从库配置
    mysql_slave_host: str = "localhost"
    mysql_slave_port: int = 3306
    mysql_slave_user: str = "root"
    mysql_slave_password: str = ""
    mysql_slave_database: str = "city_vehicle_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()