from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# 添加項目根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 導入你的模型
from models import Base
from database import engine

# 這是 Alembic 配置對象
config = context.config

# 設置 SQLAlchemy URL
config.set_main_option('sqlalchemy.url', str(engine.url))

# 設置目標元數據
target_metadata = Base.metadata

def run_migrations_offline():
    """在 'offline' 模式下運行遷移"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """在 'online' 模式下運行遷移"""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
