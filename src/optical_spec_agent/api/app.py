"""FastAPI application factory."""

from fastapi import FastAPI

from optical_spec_agent import __version__
from optical_spec_agent.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="optical-spec-agent",
        version=__version__,
        description="Convert natural language optical task descriptions into validated specs.",
    )
    app.include_router(router)
    return app


app = create_app()
