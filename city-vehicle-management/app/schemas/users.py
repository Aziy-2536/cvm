from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from pydantic import BaseModel, Field, model_validator
from datetime import datetime, date


UsernameStr = Annotated[str, Field(..., min_length=8, max_length=30, description="用户名，长度1-50")]
PhoneStr = Annotated[str, Field(..., min_length=11, max_length=16, description="电话号码，长度11-16")]
PasswordStr = Annotated[str, Field(..., min_length=8, max_length=30, description="密码，长度8-30")]
ConfirmPasswordStr = Annotated[str, Field(..., min_length=8, max_length=30, description="确认密码，长度8-30")]

class UserRegisterRequest(BaseModel):
    username: UsernameStr 
    phone: PhoneStr
    password: PasswordStr
    confirm_password: ConfirmPasswordStr
    start_time: datetime
    end_time: datetime

    #在整个模型层面进行校验，可以访问所有字段的最终值，
    # 能避免因字段定义顺序造成的各种问题，
    # 是处理复杂逻辑时最高效的兜底方案。
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegisterRequest':
        if self.confirm_password != self.password:
            raise ValueError('两次输入的密码不一致')
        return self

class UserRegisterResponse(BaseModel):
    id: int
    username: str
    phone: str
    role_level: int
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True   # 允许从 ORM 对象转换

class UserRequest(BaseModel):
    username: UsernameStr 
    password: PasswordStr
    start_time: datetime
    end_time: datetime


class UserInfoResponse(BaseModel):
    id: int
    username: str
    phone: str
    employee_id: str
    role_level: int
    hire_date: date   # 需要 from datetime import date
    start_time: datetime
    end_time: datetime

class UserAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role_level: int
    start_time: datetime
    end_time: datetime