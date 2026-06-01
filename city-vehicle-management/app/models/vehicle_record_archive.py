from datetime import datetime
from sqlalchemy import String, SmallInteger, DateTime, Float, ForeignKey, PrimaryKeyConstraint, Index,BigInteger
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.models.vehicle import Camera


class Base(DeclarativeBase):
    """所有模型的基类（保持干净）"""
    pass

class VehicleRecord(Base):

    __tablename__ = 'vehicle_records'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'pass_time'),   # 复合主键，满足分区表要求
        Index('idx_plate_pass', 'plate_number', 'pass_time'),
        Index('idx_camera_pass', 'camera_id', 'pass_time'),
        Index('idx_region_pass', 'region_code', 'pass_time'),
    )

    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="自增主键")
    id:Mapped[BigInteger] = mapped_column (BigInteger, nullable=False, autoincrement=True)
    pass_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False,
                                                 comment="通过时间"
                                                 )
    region_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="区域编码")
    plate_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True,
                                               comment="车牌号码"
                                               )
    plate_color: Mapped[str] = mapped_column(String(20), nullable=True, comment="车牌颜色")
    vehicle_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="车辆类型")
    special_vehicle_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, 
                                                                comment="特殊车辆类型"
                                                                )
    confidence: Mapped[float] = mapped_column(Float, nullable=False, comment="识别置信度")
    # 外键关联摄像头（重要！）
    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id"), 
        nullable=False, 
        index=True,
        comment="关联的摄像头ID"
    )
    
    location_address: Mapped[str] = mapped_column(String(255), nullable=False, comment="通行地点")
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
