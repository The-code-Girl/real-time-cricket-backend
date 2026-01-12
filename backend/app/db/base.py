# 👉 All models will inherit from Base.

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User