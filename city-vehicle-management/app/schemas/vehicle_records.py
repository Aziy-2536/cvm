from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class UserSelectRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    region_code: Optional[str] = None
    plate_number: Optional[str] = None
    camera_code: Optional[str] = None
    days: int = 30          # 为按车牌查询添加默认天数
    offset: int = 0
    limit: int = 300