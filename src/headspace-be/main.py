from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from routes import router as projects_router

# Create FastAPI app
app = FastAPI(
    title="Headspace Backend",
    description="FastAPI backend for the Headspace project portfolio",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",  # Alternative port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://10.10.10.187:3000",  # Your server IP
        "http://10.10.10.187:3001",  # Your server IP alternative port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(projects_router, prefix="/api", tags=["projects"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Headspace Backend is running"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Headspace Backend",
        "docs": "/api/docs",
        "version": "0.1.0"
    }

# Serve static files for frontend (when built)
frontend_dist = Path("../headspace-fe/dist")
if frontend_dist.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dist)), name="static")
    
    @app.get("/app/{path:path}")
    async def serve_frontend(path: str):
        """Serve frontend application"""
        file_path = frontend_dist / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        # Return index.html for SPA routing
        return FileResponse(frontend_dist / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 