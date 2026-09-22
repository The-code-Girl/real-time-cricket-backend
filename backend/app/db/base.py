from app.db.registry import Base

# Import all models here so Alembic sees them.
from app.models.user import User
from app.match.models import Match
