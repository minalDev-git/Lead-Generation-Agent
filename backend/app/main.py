from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Lead Generation Agent",
    version="1.0.0",
    # lifespan=lifespan,
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Lead Generation Agent API is running."
    }