from fastapi import APIRouter, Depends, HTTPException
from backend.crud import UserRepository, TieRepository, TailRepository, TaleRepository
from backend.routers.depends import Context, get_context, get_current_user, is_authenticated_api
from backend.models.schemas import (UserCreate, TieCreate, TieUpdate, TieDelete, TailCreate, TailUpdate, TailDelete,
                                    TaleCreate, TaleUpdate)


public = APIRouter()
authed = APIRouter(dependencies=[Depends(get_current_user), Depends(is_authenticated_api)])
router = APIRouter(prefix='/api/v1', tags=["CRUD operations"], dependencies=[Depends(get_context)])

#suka
@public.post("/create_user")
async def create_user(payload: UserCreate, context: Context = Depends(get_context)):
    try:
        new_user = await UserRepository.create(session=context.db, **payload.model_dump())
        return {"status": "success", "id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка базы данных: {str(e)}")

@authed.post("/create-tie")
async def create_tie(payload: TieCreate, context: Context = Depends(get_context)):
    try:
        new_tie = await TieRepository.create(session=context.db, **payload.model_dump(), user_id=context.user.id)
        return {"status": "success", "id": new_tie.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка базы данных: {str(e)}")

@authed.post("/create-tail")
async def create_tail(payload: TailCreate, context: Context = Depends(get_context)):
    try:
        new_tail = await TailRepository.create(session=context.db, **payload.model_dump(), user_id=context.user.id)
        return {"status": "success", "id": new_tail.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка базы данных: {str(e)}")

@authed.post("/create-tale")
async def create_tale(payload: TaleCreate, context: Context = Depends(get_context)):
    try:
        new_tale = await TaleRepository.create(session=context.db, **payload.model_dump(), user_id=context.user.id)
        return {"status": "success", "id": new_tale.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка базы данных: {str(e)}")

@authed.patch("/update-tale")
async def update_tale(payload: TaleUpdate, context: Context = Depends(get_context)):
    tale = await TaleRepository.update(session=context.db, **payload.model_dump(), user_id=context.user.id)
    if tale:
        return {"status": "success", "id": tale.id}
    else:
        return {"status": "fail"}

@authed.patch("/update-tail")
async def update_tail(payload: TailUpdate, context: Context = Depends(get_context)):
    tail = await TailRepository.update(session=context.db, **payload.model_dump(), user_id=context.user.id)
    if tail:
        return {"status": "success", "id": tail.id}
    else:
        return {"status": "fail"}

@authed.patch("/update-tie")
async def update_tie(payload: TieUpdate, context: Context = Depends(get_context)):
    tie = await TieRepository.update(session=context.db, **payload.model_dump(), user_id=context.user.id)
    if tie:
        return {"status": "success", "id": tie.id}
    else:
        return {"status": "fail"}

@authed.get("/tails")
async def get_tails(tie_id: int, context: Context = Depends(get_context)):
    return await TailRepository.tails(session=context.db, tie_id=tie_id, user_id=context.user.id)

@authed.delete("/delete-tie")
async def delete_tie(payload: TieDelete, context: Context = Depends(get_context)):
    print("wanafuck!")
    tie = await TieRepository.delete(session=context.db, **payload.model_dump(), user_id=context.user.id)
    return {"status": "success", "id": tie.id}

@authed.delete("/delete-tail")
async def delete_tail(payload: TailDelete, context: Context = Depends(get_context)):
    deleted = await TailRepository.delete(session=context.db, **payload.model_dump(), user_id=context.user.id)
    print('>>>', deleted)
    return {"status": "success", "deleted": bool(deleted)}


router.include_router(public)
router.include_router(authed)