from frontend.svg import SVG_ICONS
from fastapi import APIRouter, Response
from starlette.responses import FileResponse

"""Генерация псевдофайла с svg-переменными и прочие спец-роуты"""

router = APIRouter()

@router.get("/assets/svg-assets.css")
async def get_svg_icons_css():
    svg_vars = "\n\t".join([f"--{name}: {url_code};" for name, url_code in SVG_ICONS.items()])
    css_content = f":root {{\n\t{svg_vars}\n}}"
    #
    return Response(
        content=css_content,
        media_type="text/css",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )

@router.get("/favicon.ico")
async def get_favicon():
    return FileResponse(
        "frontend/static/favicon.svg",
        media_type="image/svg+xml"
    )

@router.get("/robots.txt")
async def get_robots():
    return FileResponse(
        "frontend/static/robots.txt",
        media_type="text/plain"
    )
