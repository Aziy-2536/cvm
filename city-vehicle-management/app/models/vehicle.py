from datetime import datetime
from sqlalchemy import String, SmallInteger, DateTime, Float, ForeignKey,Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ==================== 基类 ====================
class Base(DeclarativeBase):
    """所有模型的基类（保持干净）"""
    pass


# ==================== 摄像头表 ====================
class Camera(Base):
    __tablename__ = 'cameras'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")
    camera_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, 
                                             comment="摄像头编号")
    location: Mapped[str] = mapped_column(String(255), nullable=False, comment="摄像头位置")
    region: Mapped[str] = mapped_column(String(100), nullable=False, comment="所在区域")
    latitude: Mapped[float] = mapped_column(Float, nullable=True, comment="纬度")
    longitude: Mapped[float] = mapped_column(Float, nullable=True, comment="经度")
    status: Mapped[int] = mapped_column(
        SmallInteger, 
        nullable=False, 
        default=0, 
        comment="状态：0-正常, 1-故障, 2-维护中, 3-离线, 9-报废"
    )
    last_online_time: Mapped[datetime] = mapped_column(DateTime, nullable=True, 
                                                       comment="最后上线时间")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now, 
        nullable=False, 
        comment="创建时间"
    )

    # 关联车辆记录
    records: Mapped[list["VehicleRecord"]] = relationship("VehicleRecord", 
                                                          back_populates="camera")


# ==================== 车辆通行记录表 ====================
class VehicleRecord(Base):
    __tablename__ = 'vehicle_records'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")
    plate_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True,
                                               comment="车牌号码")
    plate_color: Mapped[str] = mapped_column(String(20), nullable=True, comment="车牌颜色")
    vehicle_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="车辆类型")
    special_vehicle_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, 
                                                                comment="特殊车辆类型")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, comment="识别置信度")
    
    # 外键关联摄像头（重要！）
    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id"), 
        nullable=False, 
        index=True,
        comment="关联的摄像头ID"
    )
    
    localtion_address: Mapped[str] = mapped_column(String(255), nullable=False, 
                                                   comment="通行地点")
    pass_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, 
                                                comment="通过时间")
    direction: Mapped[str] = mapped_column(String(20), nullable=False, comment="行驶方向")
    image_url: Mapped[str] = mapped_column(String(255), nullable=False, comment="车辆图片URL")
    status: Mapped[int] = mapped_column(
        SmallInteger, 
        nullable=False, 
        default=0, 
        comment="记录状态：0-正常通行, 1-黑名单, 2-异常车辆, 3-套牌嫌疑, 4-重点关注, 9-已处理"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now, 
        nullable=False, 
        comment="记录创建时间"
    )

    # 关联摄像头对象
    camera: Mapped["Camera"] = relationship("Camera", back_populates="records")


# from datetime import date
# from typing import Optional
# from sqlalchemy import Column, Integer, String, SmallInteger, Date, Index
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from datetime import datetime, DateTime



# class Base(DeclarativeBase):
#     camera_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="摄像头编号")


# class cameras(Base):
#     __tablename__ = 'cameras'

#     __table_args__ = (
#         Index('camera_code_UNIQUE', 'camera_code'),
#         Index('id_UNIQUE', 'id'),
#     )

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")   
#     location: Mapped[str] = mapped_column(String(255), nullable=False, comment="摄像头位置")
#     region: Mapped[str] = mapped_column(String(255), nullable=False, comment="摄像头所在区域")
#     latitude: Mapped[str] = mapped_column(String(50), nullable=False, comment="摄像头纬度")
#     longitude: Mapped[str] = mapped_column(String(50), nullable=False, comment="摄像头经度")
#     status: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, comment="摄像头状态：0-正常，1-故障，2-维护中,3-离线,9-报废")
#     last_online_time: Mapped[date] = mapped_column(Date, nullable=False, comment="最后上线时间")
#     # created_at: Mapped[date] = mapped_column(Date, nullable=False, comment="创建时间")
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")


# class vehicle_records(Base):
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")
#     plate_number: Mapped[str] = mapped_column(String(20), nullable=False, comment="车牌号码")
#     vehicle_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="车辆类型")
#     special_vehicle_type:Mapped[str] = mapped_column(String(50), nullable=True, comment="特殊车辆类型")
#     confidence: Mapped[float] = mapped_column(nullable=False, comment="识别置信度")
#     pass_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="通过时间")
#     direction: Mapped[str] = mapped_column(String(50), nullable=False, comment="行驶方向")
#     image_url: Mapped[str] = mapped_column(String(255), nullable=False, comment="车辆图片URL")
#     status: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, comment="记录状态：0-正常通行, 1-黑名单, 2-异常车辆, 3-套牌嫌疑,4，重点关注， 9-已处理")
#     creted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="记录创建时间")

