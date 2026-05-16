"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from optical_spec_agent import __version__
from optical_spec_agent.api.routes import router

LOCAL_FRONTEND_ORIGINS = (
    "http://127.0.0.1:5173",
    "http://localhost:5173",
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="optical-spec-agent",
        version=__version__,
        description="Convert natural language optical task descriptions into validated specs.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(LOCAL_FRONTEND_ORIGINS),
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )
    app.include_router(router)
    return app


app = create_app()
