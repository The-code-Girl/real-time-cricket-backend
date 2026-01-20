import sys
import os
from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

load_dotenv()

# Add 'backend' folder to path so 'app' can be imported
# __file__ is migrations/env.py, so go up 1 folder to 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.base import Base  # Base includes all your models

target_metadata = Base.metadata


config = context.config
fileConfig(config.config_file_name)

# Override DB URL from .env if available
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
