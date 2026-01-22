import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import infrastructure
from src.infrastructure.config.settings import get_settings
from src.infrastructure.config.container import get_container
from src.infrastructure.web.ticket_router import router as ticket_router

# Startup time for uptime calculation
startup_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    settings = get_settings()
    container = get_container()
    
    print("🚀 AI-Powered Support Co-Pilot starting...")
    print(f"📝 Environment: {settings.environment}")
    print(f"🗄️  Database: {'In-Memory' if settings.use_in_memory_db else 'Supabase'}")
    print(f"🤖 AI Service: {'Gemini' if settings.has_gemini_config else 'Not configured'}")
    print(f"🔗 WebSocket: Enabled")
    
    yield
    
    # Shutdown
    print("🛑 AI-Powered Support Co-Pilot shutting down...")

# Create FastAPI app with new architecture
app = FastAPI(
    title="AI-Powered Support Co-Pilot",
    description="Intelligent ticket processing with AI categorization and sentiment analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add process time header middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include main router
app.include_router(ticket_router, prefix="/api/v1", tags=["AI Support Co-Pilot"])

@app.get("/")
async def root():
    """
    Root endpoint with system information
    """
    settings = get_settings()
    uptime = time.time() - startup_time
    
    return {
        "message": "AI-Powered Support Co-Pilot API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.environment,
        "uptime_seconds": round(uptime, 2),
        "endpoints": {
            "health": "/api/v1/health",
            "process_ticket": "/api/v1/process-ticket",
            "tickets": "/api/v1/tickets",
            "websocket": "/api/v1/ws",
            "docs": "/docs"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    settings = get_settings()
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.is_development else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development
    )

