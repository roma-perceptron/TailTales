from fastapi import FastAPI
from backend.config import BASE_PATH
from fastapi.staticfiles import StaticFiles
from backend.routers.api import router as api_router
from backend.routers.web import router as web_router
from backend.routers.auth import router as auth_router
from backend.routers.assets import router as assets_router
from backend.exceptions import html_404_handler, html_500_handler


api_metadata = [
    {"name": "CRUD operations", "description": "Все для создания и управления данными в БД"},
    {"name": "AUTH operations", "description": "Регистрация, авторизация, вход и выход пользователя"},
    {"name": "WEB pages", "description": "Хосты веб-страниц"},
]

app = FastAPI(
    title="TailTales API",
    description="Секрет для входа хранится в APIKeyCookie. Поэтому для тестов закрытых методов необходимо авторизоваться"
                " через /auth/login, либо через интерфейсную форму на главной пользовательской странице. ",
    swagger_ui_parameters={"docExpansion": "none"},
    openapi_tags=api_metadata,
)

app.mount("/static", StaticFiles(directory=BASE_PATH / "frontend/static"), name="static")
app.add_exception_handler(404, html_404_handler)
app.add_exception_handler(500, html_500_handler)


app.include_router(auth_router)
app.include_router(api_router)
app.include_router(web_router)
app.include_router(assets_router, include_in_schema=False)
