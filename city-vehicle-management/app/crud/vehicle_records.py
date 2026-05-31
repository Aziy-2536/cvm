from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List
from app.models.vehicle import VehicleRecord
from app.models.vehicle import Camera
from datetime import datetime, timedelta


async def query_vehicle_records(
        db:AsyncSession,
        start_time: datetime,
        end_time: datetime,
        region_code: str | None = None,
        plate_number: str | None = None,
        camera_id: int | None = None,
        offset: int = 0,
        limit: int |None = 300
) -> List[VehicleRecord]:
    """根据多个条件查询车辆通行记录"""
    stms = select(VehicleRecord).where(
        VehicleRecord.pass_time.between(start_time, end_time)
    )
    if region_code:
        stms = stms.where(VehicleRecord.region_code == region_code)
    if plate_number:
        stms = stms.where(VehicleRecord.plate_number == plate_number)
    if camera_id:
        stms = stms.where(VehicleRecord.camera_id == camera_id)
    
    stms = stms.order_by(VehicleRecord.pass_time.desc()).offset(offset)
    if limit is not None:
        stms = stms.limit(limit)

    result = await db.execute(stms)
    records = result.scalars().all()
    return records


async def get_vehicle_records_by_plate_number(
    db: AsyncSession, 
    plate_number: str,
    days: int = 30,
    offset: int = 0,
    limit: int = 100
) -> List[VehicleRecord]:
    """根据车牌号码查询近N天车辆通行记录（便捷方法）"""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    # 复用通用查询函数
    return await query_vehicle_records(
        db=db,
        start_time=start_time,
        end_time=end_time,
        plate_number=plate_number,
        offset=offset,
        limit=limit
    )

async def get_vehicle_records_by_camera_code(
    db: AsyncSession,
    camera_code: str,
    start_time: datetime,
    end_time: datetime,
    offset: int = 0,
    limit: int | None = 300
) -> List[VehicleRecord]:
    """
    根据 camera_code 和时间范围查询过车记录
    """
    # 1. 查询 cameras 表获取对应的 id
    result = await db.execute(
        select(Camera.id).where(Camera.camera_code == camera_code)
    )
    camera_id = result.scalar_one_or_none()
    if camera_id is None:
        return []   # 摄像头不存在，返回空列表
    
    # 2. 复用通用查询
    return await query_vehicle_records(
        db=db,
        start_time=start_time,
        end_time=end_time,
        camera_id=camera_id,
        offset=offset,
        limit=limit
    )

# async def insert_vehicle_record(
#     db: AsyncSession,
#     plate_number: str,
#     region_code: str,
#     camera_id: int,
#     pass_time: datetime
# ) -> VehicleRecord:
#     """插入新的车辆通行记录"""
#     new_record = VehicleRecord(
#         plate_number=plate_number,
#         region_code=region_code,
#         camera_id=camera_id,
#         pass_time=pass_time
#     )
#     db.add(new_record)
#     await db.commit()
#     await db.refresh(new_record)
#     return new_record

# # 在调试时，获取原始 SQL 并手动加上 EXPLAIN
# from sqlalchemy import text
# async with db as conn:
#     result = await conn.execute(text("EXPLAIN " + str(stms)))
#     print(result.fetchall())

# async def get_vehicle_records_by_plate_number(
#         db: AsyncSession, 
#         plate_number: str,
#         days: int = 30,
#         offset: int = 0,
#         limit: int = 100
#         ) -> List[VehicleRecord]:
#     '''函数返回一个列表，列表中的每个元素都是 VehicleRecord 类型的对象
#     （即 ORM 模型实例'''
#     """根据车牌号码查询车辆通行记录"""

#     end_time = datetime.now()
# # timedelta(days=30) 表示一个 30 天的时间长度
#     start_time = end_time - timedelta(days=days)

#     stmt = (
# # '''创建一个 SELECT 查询，
# # 目标是从 vehicle_records 表（通过 ORM 模型 VehicleRecord 映射）
# # 中选取所有列（等价于 SELECT *）'''
#         select(VehicleRecord)
# #添加过滤条件。这里有两个条件用逗号分隔，相当于 SQL 中的 AND
# # VehicleRecord.plate_number == plate_number匹配车牌号。
# # VehicleRecord.pass_time.between(start_time, end_time)
# # 限定过车时间在 start_time 和 end_time 之间。
#         .where(
#             VehicleRecord.plate_number == plate_number,
#             VehicleRecord.pass_time.between(start_time,end_time)
#         )
# # 按 pass_time 降序排列，让最新的记录排在前面（符合业务习惯）。
#         .order_by(VehicleRecord.pass_time.desc())
#         .offset(offset)
#         .limit(limit)
#     )
#     result = await db.execute(stmt)
# #.scalars() 将 Result 对象转换为一个 ScalarResult，
# # 它只返回每行的第一列（由于我们 select(VehicleRecord)，
# # 整行就是一个 VehicleRecord 对象，
# # 所以 scalars() 提取的就是这些对象）。
# #.all() 将所有对象收集到一个 Python 列表中。
#     records = result.scalars().all()
#     return records







# async def get_vehicle_records_by_time(
#         db: AsyncSession, 
#         start_time: datetime,
#         end_time: datetime,
#         offset: int = 0,
#         limit: int | None = None
#         ) -> List[VehicleRecord]:
#     """根据时间范围查询车辆通行记录"""
#     stmt = (
#         select(VehicleRecord).where(
#             VehicleRecord.pass_time.between(start_time, end_time)
#         ).order_by(VehicleRecord.pass_time.desc()).offset(offset)
#     )
#         if limit is not None :
#             stmt = stmt.limit(limit)
        
#         result = await db.execute(stmt)
#         records = result.scalars().all()
#         return records
#     )
# )   

# async def get_vehicle_records_by_time(
#     db: AsyncSession, 
#     start_time: datetime,
#     end_time: datetime,
#     offset: int = 0,
#     limit: int | None = None
# ) -> List[VehicleRecord]:
#     """根据时间范围查询车辆通行记录"""
#     stmt = (
#         select(VehicleRecord)
#         .where(VehicleRecord.pass_time.between(start_time, end_time))
#         .order_by(VehicleRecord.pass_time.desc())
#         .offset(offset)
#     )
    
#     if limit is not None:
#         stmt = stmt.limit(limit)
    
#     result = await db.execute(stmt)
#     records = result.scalars().all()
#     return records

# async def get_vehicle_records_by_region_code(
#     db: AsyncSession, 
#     region_code: str,
#     start_time: datetime,
#     end_time: datetime,
#     offset: int = 0,
#     limit: int = 300
# ) -> List[VehicleRecord]:
#     """根据区域编码和时间范围查询车辆通行记录"""
#     stmt = (
#         select(VehicleRecord)
#         .where(VehicleRecord.pass_time.between(start_time, end_time))
#         .where(VehicleRecord.region_code == region_code)
#         .order_by(VehicleRecord.pass_time.desc())
#             .offset(offset)
#         )
#     if limit is not None:
#         stmt = stmt.limit(limit)
    
#     result = await db.execute(stmt)
#     records = result.scalars().all()
#     return records