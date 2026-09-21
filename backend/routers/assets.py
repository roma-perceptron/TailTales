from frontend.svg import SVG_ICONS
from fastapi import APIRouter, Response

"""Генерация псевдофайла с svg-переменными"""

router = APIRouter()

@router.get("/assets/svg-assets.css")
def get_svg_icons_css():
    svg_vars = "\n\t".join([f"--{name}: {url_code};" for name, url_code in SVG_ICONS.items()])
    css_content = f":root {{\n\t{svg_vars}\n}}"

    #
    return Response(
        content=css_content,
        media_type="text/css",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )
