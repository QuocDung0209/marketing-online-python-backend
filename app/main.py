from starlette.middleware.cors import CORSMiddleware

from app.core.application import ApplicationBase
from app.core.config import settings

# from app.models import models

# from app.db.session import engine

# Create all tables in the database.
# Comment this out if you using migrations.
# models.Base.metadata.create_all(bind=engine)

app = ApplicationBase(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=False,
    version="1.0",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
