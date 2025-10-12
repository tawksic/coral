from fastapi import FastAPI

from app.api.routes import health, container, simulation

app = FastAPI()

# Include routers
app.include_router(health.router)
app.include_router(container.router)
app.include_router(simulation.router)
