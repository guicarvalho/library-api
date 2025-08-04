from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.endpoints import book, review, user
from app.api.routes import router as health_check_router
from app.exceptions import GenericError


def create_app() -> FastAPI:
    app = FastAPI(title="My Library API")
    configure_routes(app)
    configure_exception_handlers(app)
    return app


def configure_routes(app: FastAPI) -> None:
    app.include_router(health_check_router)
    app.include_router(user.router)
    app.include_router(book.router)
    app.include_router(review.router)


def configure_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(GenericError)
    async def _(_: Request, exc: GenericError):
        return JSONResponse(
            status_code=HTTPStatus(exc.code or 500),
            content={"detail": exc.detail},
        )


app = create_app()
