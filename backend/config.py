import os
import time
import pathlib
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates


# корень проекта
BASE_PATH = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(BASE_PATH / ".env")


# MySQL
DB_HOST = os.getenv("DB_HOST")
DB_PASS = os.getenv("DB_PASS")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
DB_URL_SYNC = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL_ASYNC = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# шаблоны
templates = Jinja2Templates(directory=BASE_PATH / "frontend/templates")
templates.env.globals["APP_VERSION"] = int(time.time())