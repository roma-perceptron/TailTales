import secrets
from backend import utils
from starlette import status
from fastapi import APIRouter, Depends
from backend.crud import UserRepository
from fastapi import Response, HTTPException
from fastapi.responses import RedirectResponse
from backend.models.schemas import TokenResponse, TokenRequest
from backend.routers.depends import Context, get_context, get_current_user, is_authenticated_web

public = APIRouter()
authed = APIRouter(dependencies=[Depends(get_current_user), Depends(is_authenticated_web)])
router = APIRouter(prefix="/auth", tags=["AUTH operations"], dependencies=[Depends(get_context)])


@public.get("/register", response_model=TokenResponse)
async def register_anonymous_user(response: Response, context: Context = Depends(get_context)):
    raw_token = secrets.token_urlsafe(32).replace('-', 'x') # просто бесят дефисы недающие выделить кликом
    hashed = utils.hash_token(raw_token)
    #
    user = await UserRepository.create(context.db, hashed_token=hashed)
    response.set_cookie(key="auth_token", value=raw_token, httponly=True, max_age=315360000, samesite="lax")
    #
    return {
        "token": raw_token,
        "message": "Сохрани этот токен! Вход только по нему.",
        "user_id": user.id
    }


@public.post("/login")
async def login(payload: TokenRequest, response: Response, context: Context = Depends(get_context)):
    token = payload.token
    #
    hashed = utils.hash_token(token)
    user = await UserRepository.get(context.db, hashed)
    if not user:
            raise HTTPException(status_code=401, detail="Неверный токен")
    else:
        response.set_cookie(key="auth_token", value=token, httponly=True, max_age=315360000, samesite="lax")
        return {"ok": True, "redirect_url": "/ties"}


@authed.get("/logout")
async def logout(context: Context = Depends(get_context)):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="auth_token", httponly=True, samesite="lax")
    return response


@authed.get("/test_auth")
async def read_secure_data(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "user": current_user}


router.include_router(public)
router.include_router(authed)
