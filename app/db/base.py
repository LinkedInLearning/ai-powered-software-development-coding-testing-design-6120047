from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so Alembic can discover them via Base.metadata
# isort: off
from ..models import user, expense, category  # noqa: F401
