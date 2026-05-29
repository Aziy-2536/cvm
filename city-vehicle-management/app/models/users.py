# from datetime import datetime
# from typing import Optional

# from sqlalchemy import Column, Integer, String, SmallInteger, Date, Index
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import date
from typing import Optional
from sqlalchemy import Column, Integer, String, SmallInteger, Date, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    """
    用户信息表ORM模型
    """
    __tablename__ = 'users'

    # 创建索引
    __table_args__ = (
        Index('username_UNIQUE', 'name'),
        Index('phone_UNIQUE', 'phone'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="姓名")
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment="电话号码")
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="职工编号")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希值")
    role_level: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, comment="权限等级：0-普通，1-主管，2-管理员，9-超级管理员")
    hire_date: Mapped[date] = mapped_column(Date, nullable=False, comment="入职时间")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, employee_id={self.employee_id})>"