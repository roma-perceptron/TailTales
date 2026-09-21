from fastapi import Request
from backend.config import templates
from starlette.exceptions import HTTPException as StarletteHTTPException

path_prefix = "/errors/"


async def html_404_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(
        request=request,
        name=f"{path_prefix}404.html",
        context={"detail": exc.detail},
        status_code=404
    )


async def html_500_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request,
        name="500.html",
        context={"error": "Внутренняя ошибка сервера"},
        status_code=500
    )
