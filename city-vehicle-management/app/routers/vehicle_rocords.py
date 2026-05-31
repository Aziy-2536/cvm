from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db_conf import get_db
from app.schemas.vehicle_records import UserSelectRequest
from app.utils.response import success_response
from app.crud.vehicle_records import (
    query_vehicle_records,
    get_vehicle_records_by_plate_number,
    get_vehicle_records_by_camera_code
)


router = APIRouter(prefix="/api/vehicle_rocords", tags=["vehicle_rocords"])

# @router.post("/select",response_model=UserSelectRequest, status_code=status.HTTP_200_OK)
# async def User_select_region_code_plate_number(user_data: UserSelectRequest, db: AsyncSession = Depends(get_db)):
#     # 检查用户是否已存在
#     result = await query_vehicle_records(
#         db=db,
#         start_time=user_data.start_time,
#         end_time=user_data.end_time,
#         region_code=user_data.region_code,
#         plate_number=user_data.plate_number,
#         camera_code=user_data.camera_code,
#         offset=user_data.offset,
#         limit=user_data.limit
#     )
#     if not result:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="查询结果不存在")
#     return result

@router.post("/select", status_code=status.HTTP_200_OK)
async def select_vehicle_records(
    req: UserSelectRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await query_vehicle_records(
        db=db,
        start_time=req.start_time,
        end_time=req.end_time,
        region_code=req.region_code,
        plate_number=req.plate_number,
        camera_id=None,          # 注意：这里需要 camera_id，但请求中是 camera_code
        # 如果需要处理 camera_code，应在函数内转换
        offset=req.offset,
        limit=req.limit
    )
    # 直接返回结果（空列表也是正常响应）
    return result

# @router.post("/select-by-plate",response_model=UserSelectRequest, status_code=status.HTTP_200_OK)
# async def User_get_vehicle_records_by_plate_number(user_data: UserSelectRequest, db: AsyncSession = Depends(get_db)):
#     # 根据根据车牌号码查询近N天车辆通行记录
#     result = await get_vehicle_records_by_plate_number(
#         db=db,
#         plate_number=user_data.plate_number,
#         days=user_data.days,
#         offset=user_data.offset,
#         limit=user_data.limit
#     )
#     if not result:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="查询结果不存在")
#     return result

# 按车牌查询（便捷接口）
@router.post("/select-by-plate", status_code=status.HTTP_200_OK)
async def select_by_plate(
    req: UserSelectRequest,
    db: AsyncSession = Depends(get_db)
):
    # 注意：需要确保 req 中有 plate_number 和 days
    result = await get_vehicle_records_by_plate_number(
        db=db,
        plate_number=req.plate_number,
        days=req.days,
        offset=req.offset,
        limit=req.limit
    )
    return result



# @router.post("/select-by-camera",response_model=UserSelectRequest, status_code=status.HTTP_200_OK)
# async def User_get_vehicle_records_by_camera_code(user_data: UserSelectRequest, db: AsyncSession = Depends(get_db)):
#     # 根据根据摄像头编号查询近N天车辆通行记录
#     result = await get_vehicle_records_by_camera_code(
#         db=db,
#         camera_code=user_data.camera_code,
#         start_time=user_data.start_time,
#         end_time=user_data.end_time,
#         offset=user_data.offset,
#         limit=user_data.limit
#     )
#     if not result:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="查询结果不存在")
#     return result
# 按摄像头代码查询
@router.post("/select-by-camera", status_code=status.HTTP_200_OK)
async def select_by_camera(
    req: UserSelectRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await get_vehicle_records_by_camera_code(
        db=db,
        camera_code=req.camera_code,
        start_time=req.start_time,
        end_time=req.end_time,
        offset=req.offset,
        limit=req.limit
    )
    return result