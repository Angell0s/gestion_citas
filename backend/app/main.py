# backend\app\main.py
from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(api_router, prefix="/api/v1")


# punto de entrada cuando se ejecuta directamente
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
