# app/utils/generator.py
import uuid

def generate_employee_id() -> str:
    """生成一个唯一的员工编号"""
    # 可以用 UUID 的简单形式，例如 'EMP-' + uuid.uuid4().hex[:8].upper()
    return f"EMP-{uuid.uuid4().hex[:8].upper()}"