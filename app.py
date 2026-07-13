from fastapi import FastAPI

app = FastAPI(
    title="Dahab AI Assistant",
    description="AI-powered WhatsApp assistant for apartment guests.",
    version="1.0.0",
)


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint.
    Used to verify that the application is running.
    """
    return {
        "project": "Dahab AI Assistant",
        "status": "running",
        "version": app.version,
    }


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint.
    Used by monitoring systems to verify application health.
    """
    return {
        "status": "healthy",
    }