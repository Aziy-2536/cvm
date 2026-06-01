from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vehicle import VehicleRecord
from app.models.vehicle_record_archive import VehicleRecord

async def archive_old_partitions(db: AsyncSession, months_to_keep: int = 24):
    """
    将超过 months_to_keep 个月的分区数据复制到归档表，并删除原分区。
    同时创建下个月的分区（如果尚未存在）。
    """
    # 1. 计算要归档的月份（当前日期减去 months_to_keep 个月）
    target_date = datetime.now() - timedelta(days=months_to_keep * 30)  # 近似
    archive_year = target_date.year
    archive_month = target_date.month
    partition_name = f"p{archive_year}{archive_month:02d}"

    # 2. 检查分区是否存在
    check_sql = text("""
        SELECT 1 FROM information_schema.partitions
        WHERE table_schema = DATABASE()
          AND table_name = 'vehicle_records'
          AND partition_name = :part_name
    """)
    result = await db.execute(check_sql, {"part_name": partition_name})
    if not result.scalar_one_or_none():
        return {"message": f"Partition {partition_name} does not exist, skip archive."}

    # 3. 复制数据到归档表（使用原生SQL，因为PARTITION语法ORM不支持）
    copy_sql = text(f"""
        INSERT INTO vehicle_records_archive
        SELECT * FROM vehicle_records PARTITION({partition_name})
    """)
    await db.execute(copy_sql)
    await db.commit()

    # 4. 删除该分区
    drop_sql = text(f"ALTER TABLE vehicle_records DROP PARTITION {partition_name}")
    await db.execute(drop_sql)
    await db.commit()

    # 5. 创建下个月的分区（确保未来分区存在）
    next_month = datetime.now().replace(day=1) + timedelta(days=32)
    next_month = next_month.replace(day=1)
    next_partition_name = f"p{next_month.year}{next_month.month:02d}"
    next_boundary = (next_month + timedelta(days=32)).replace(day=1)

    # 检查是否已存在
    result = await db.execute(check_sql, {"part_name": next_partition_name})
    if not result.scalar_one_or_none():
        add_sql = text(f"""
            ALTER TABLE vehicle_records
            ADD PARTITION (PARTITION {next_partition_name}
            VALUES LESS THAN ('{next_boundary.strftime('%Y-%m-%d')}'))
        """)
        await db.execute(add_sql)
        await db.commit()

    return {"archived_partition": partition_name, "created_partition": next_partition_name}