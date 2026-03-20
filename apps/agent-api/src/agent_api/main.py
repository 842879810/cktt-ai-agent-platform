"""FastAPI main application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import agents, crews, tasks

app = FastAPI(
    title="CKTT AI Agent Platform",
    description="Enterprise AI Agent Platform API",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(crews.router, prefix="/api/v1/crews", tags=["crews"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "CKTT AI Agent Platform API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
