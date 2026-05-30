# from datetime import datetime
# from typing import Optional

# from sqlalchemy import Column, Integer, String, SmallInteger, Date, Index
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import date
from typing import Optional
from sqlalchemy import Column, Integer, String, SmallInteger, Date, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, DateTime

class Base(DeclarativeBase):
    pass

class User(Base):
    """
    用户信息表ORM模型
    """
    __tablename__ = 'users'

    # 创建索引
    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")
    username: Mapped[str] = mapped_column(String(50), nullable=False, comment="姓名")
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment="电话号码")
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="职工编号")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希值")
    role_level: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, comment="权限等级：0-普通，1-主管，2-管理员，9-超级管理员")
    hire_date: Mapped[date] = mapped_column(Date, nullable=False, comment="入职时间")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, employee_id={self.employee_id})>"
    
# class cameras(Base):
#     __talbename__ = 'cameras'

#     __table_args__ = (
#         Index('camera_code_UNIQUE', 'camera_code'),
#         Index('id_UNIQUE', 'id'),
#     )

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")
#     cameras_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="摄像头编号")
#     location: Mapped[str] = mapped_column(String(255), nullable=False, comment="摄像头位置")
#     region: Mapped[str] = mapped_column(String(255), nullable=False, comment="摄像头所在区域")
#     latitude: Mapped[str] = mapped_column(String(50), nullable=False, comment="摄像头纬度")
#     longitude: Mapped[str] = mapped_column(String(50), nullable=False, comment="摄像头经度")
#     status: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, comment="摄像头状态：0-正常，1-故障，2-维护中,3-离线,9-报废")
#     last_online_time: Mapped[date] = mapped_column(Date, nullable=False, comment="最后上线时间")
#     # created_at: Mapped[date] = mapped_column(Date, nullable=False, comment="创建时间")
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")


# class vehicle_records(Base):