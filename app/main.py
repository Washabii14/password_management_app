from fastapi import FastAPI

from app.api.v1.auth_routes import router as auth_router


app = FastAPI(title="Password Manager Backend", version="0.1.0")


@app.get("/health", tags=["system"])
def health_check() -> dict:
    """
    Simple health endpoint to verify the app and dependencies are wired correctly.
    """
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/v1")



