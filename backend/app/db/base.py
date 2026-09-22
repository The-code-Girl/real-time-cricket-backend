from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so Alembic sees them.
from app.models.user import User
from app.match.models import Match
