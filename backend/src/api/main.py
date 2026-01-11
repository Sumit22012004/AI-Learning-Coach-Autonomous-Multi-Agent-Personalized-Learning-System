from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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

@app.get("/")
async def root():
    return {"message": "Welcome to AI Learning Coach API", "version": "0.1.0"}

from src.api.v1.endpoints import agents

app.include_router(agents.router, prefix="/agents", tags=["agents"])
