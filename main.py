import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import init_db
from backend.routes.auth_routes import router as auth_router
from backend.routes.chat_routes import router as chat_router
from backend.routes.resource_routes import router as resource_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("nivaaran")

# Initialize SQLite database schema
init_db()

app = FastAPI(
    title="Nivaaran API - Financial Inclusion Assistant",
    description="Backend service for Nivaaran AI Chatbot (SDG 1: No Poverty)",
    version="1.0.0"
)

# Enable CORS for local dev and frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(resource_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    """Service health check."""
    return {
        "status": "online",
        "service": "Nivaaran Financial Inclusion Assistant",
        "sdg_goal": "SDG 1: No Poverty",
        "version": "1.0.0"
    }


# Static frontend hosting if built
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
