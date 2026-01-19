from sqlalchemy.orm import declarative_base

Base = declarative_base()

# import all models here so Alembic sees them
from app.models.user import User
