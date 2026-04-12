"""FastAPI application factory."""

from fastapi import FastAPI

from optical_spec_agent.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="optical-spec-agent",
        version="0.1.0",
        description="Convert natural language optical task descriptions into validated specs.",
    )
    app.include_router(router)
    return app


app = create_app()
