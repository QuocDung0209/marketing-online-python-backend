# Import all the models, so that the Base class
# has them before being imported by Alembic.

from app.models.user import User  # noqa

from .base import Base  # noqa
