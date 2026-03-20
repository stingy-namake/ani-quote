from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.database import engine, Base
from app.routers import quotes, anime, characters
from app.config import settings


# Create tables on startup (for dev only - use Alembic in production)
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="AniQuote API",
    description="""
    A comprehensive API for anime quotes. 
    
    Features:
    - Browse quotes by anime, character, or search
    - Get random quotes
    - Full CRUD operations for anime, characters, and quotes
    - Like quotes
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(quotes.router)
app.include_router(anime.router)
app.include_router(characters.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to AniQuote API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
