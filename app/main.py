from fastapi import FastAPI
from app.routers import users

app = FastAPI(
    title="User API",
    version="1.0.0"
)

# Register routers
app.include_router(users.router, prefix="/api/v1")