"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, users, cases

# Create FastAPI app
app = FastAPI(
    title="SpyNet Backend API",
    description="Backend API for SpyNet - Detective and Manager Dashboard",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cases.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "SpyNet Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
