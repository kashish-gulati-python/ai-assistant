from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.conversations import router as conversation_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.include_router(auth_router)
app.include_router(conversation_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}
