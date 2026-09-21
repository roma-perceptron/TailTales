from backend.config import templates
from fastapi import APIRouter, Depends
from fastapi import Request, HTTPException
from backend.crud import TieRepository, TailRepository
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.models.models import TieType, TailStatusInterface
from backend.routers.depends import Context, get_context, get_current_user, is_authenticated_web


public = APIRouter()
authed = APIRouter(dependencies=[Depends(get_current_user), Depends(is_authenticated_web)])
router = APIRouter(tags=["WEB pages"], dependencies=[Depends(get_context)])


@public.get("/")
def index(request: Request, context: Context = Depends(get_context)) -> HTMLResponse:
    if context.user:
        return RedirectResponse(url="/ties")
    else:
        return templates.TemplateResponse(request, name="hello.html")


@authed.get("/ties", response_class=HTMLResponse)
async def ties_page(request: Request, context: Context = Depends(get_context)):
    types = {k: v.value for k, v in TieType.__members__.copy().items()}
    ties = await TieRepository.ties(session=context.db, user_id=context.user.id)
    context = {"user_id": context.user.id, "ties": ties, "types": types, 'user': context.user}

    return templates.TemplateResponse(request=request, name="ties.html", context=context)


@authed.get("/tie/{tie_id}", response_class=HTMLResponse)
async def tail_page(request: Request, context: Context = Depends(get_context), tie_id: int | None = None):
    tie = context.user.ties_dict.get(tie_id)
    if tie:
        tails = await TailRepository.tails(session=context.db, tie_id=tie_id, user_id=context.user.id)
        statuses = {k:v.value for k, v in TailStatusInterface.__members__.copy().items()}
        context = {"user": context.user, "tie": tie, "tails": tails, "statuses": statuses}
        return templates.TemplateResponse(request=request, name="tails.html", context=context)
    else:
        raise HTTPException(status_code=404)


router.include_router(public)
router.include_router(authed)
