from backend import utils
from starlette import status
from backend.db import get_db
from dataclasses import dataclass
from backend.models.models import User
from backend.crud import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Request


from fastapi.security import APIKeyCookie
cookie_token = APIKeyCookie(name="auth_token", auto_error=False)


"""
    Базовая идея: до каждого без исключений эндпойнта должна быть сразу прокинута переменная context: Context внутри
    которой будет поднятая сессия к бд и объект с текущим юзером. При этом первое обязательно, а второе нет.
    Но все же наличие user требуется для большинства эндпойнтов, для этого на них вешается отдельная зависимость
    определяющая пользователя по токену из куки auth_token и кидающая 401 или редирект на главную.
    
    Можно было все проверки делать сразу в get_content, но тогда технически ВСЕ роуты числились закрытми (с замками). 
    Так не хотелось, поэтому изначально user пустой. Однако даже для открытых эндпойнтов хорошо иметь знание про юзера,
    поэтому необязательная проверка на наличие куки делается сразу, но без выкидывания исключений и редиректов. 
"""


@dataclass
class Context:
    db: AsyncSession
    user: User | None = None


async def _get_current_user(request: Request, token: str, db: AsyncSession):
    if token:
        hashed = utils.hash_token(token)
        user = await UserRepository.get(db, hashed)
        if user:
            request.state.user = user
            return user


async def get_context(request: Request, db: AsyncSession = Depends(get_db)) -> Context:
    # user не обязателен, но попытка определить его по наличию куки делается вне механизм Depends,
    # чтобы в /docs не было "замков" на всех методах
    user = await _get_current_user(request, request.cookies.get("auth_token"), db)
    return Context(db=db, user=user)


async def get_current_user(request: Request, token: str = Depends(cookie_token), context: Context=Depends(get_context)):
    return await _get_current_user(request, token, context.db)


async def is_authenticated_web(context: Context=Depends(get_context)):
    if not context.user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"},
        )


async def is_authenticated_api(context: Context=Depends(get_context)):
    if not context.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Unauthorized", "message": "Пройдите авторизацию"}
        )
