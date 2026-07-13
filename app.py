from fastapi import FastAPI

from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered WhatsApp assistant for apartment guests.",
    version=settings.APP_VERSION,
)


@app.get("/", tags=["System"])
async def root():
    return {
        "project": settings.APP_NAME,
        "status": "running",
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
    }