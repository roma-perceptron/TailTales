import base64
from urllib.parse import quote as quote_for_svg


RAW_SVGS_ICONS = {
    "svg-icon-empty": '''''',
    "svg-icon-active": '''<path d="M 10.3 9.9 C 9.6 9.1, 8.2 10.2, 9.3 11.7 C 11.0 13.0, 13.6 10.8, 12.9 8.8 C 12.0 5.8, 6.2 6.5, 6.5 11.5 C 6.7 13.5, 8.5 14.5, 11.0 14.2" />''',
    "svg-icon-staged": '''  <path d="M 5.5 16.5 L 5.5 3.5 L 14.5 7.0 L 5.5 10.5" />''',
    "svg-icon-pending": '''<path d="M 10.2 3.6 C 13.7 3.4, 16.4 6.2, 16.2 9.8 C 16.0 13.4, 13.4 16.2, 9.8 16.4 C 6.2 16.6, 3.6 13.6, 3.8 10.2 C 4.0 6.6, 6.6 3.8, 10.2 3.6 Z" /><path d="M 9.7 6.8 L 10.1 10.3 L 13.2 10.0" />''',
    "svg-icon-pause": '''<path d="M 6.2 5.5 C 6.2 4.7, 7.3 4.6, 7.3 5.5 L 7.1 14.5 C 7.1 15.3, 6.0 15.4, 6.0 14.5 Z" /><path d="M 12.8 5.7 C 12.8 4.9, 13.9 4.8, 13.9 5.7 L 13.7 14.3 C 13.7 15.1, 12.6 15.2, 12.6 14.3 Z" />''',
    "svg-icon-closed": '''<path d="M 4.5 9.8 C 4.0 9.2, 4.9 8.4, 5.4 9.0 L 8.3 12.8 C 8.5 13.1, 8.9 13.1, 9.1 12.8 L 15.3 5.4 C 15.7 4.9, 16.6 5.5, 16.1 6.1 L 9.3 14.4 C 8.8 15.0, 8.0 14.9, 7.6 14.3 Z" />''',
    "svg-icon-canceled": '''<path d="M 5.3 5.2 C 4.7 4.7, 5.7 3.8, 6.3 4.3 L 14.8 14.7 C 15.3 15.3, 14.3 16.2, 13.7 15.7 Z" /><path d="M 5.2 14.6 C 4.6 15.2, 3.8 14.2, 4.3 13.6 L 14.6 5.3 C 15.2 4.7, 16.1 5.7, 15.5 6.3 Z" />''',
}

RAW_SVGS_LINES = {
    "empty": "",
    "waveline": "M0,6 C2.5,0 2.5,12 5,6 C7.5,0 7.5,12 10,6 C12.5,0 12.5,12 15,6 C17.5,0 17.5,12 20,6",
    "waveline2": "M0,6 C5,0 5,12 10,6 C15,0 15,12 20,6",
    "doubleline": "M0,4 L20,4 M0,8 L20,8",
    "tripleline": "M0,3 L20,3 M0,6 L20,6 M0,9 L20,9",
    "zigzag1": "M0,6 L5,0 L10,6 L15,12 L20,6",
    "zigzag2": "M0,6 L1.66,2 L3.33,10 L5,2 L6.66,10 L8.33,2 L10,10 L11.66,2 L13.33,10 L15,2 L16.66,10 L18.33,2 L20,6",
    "zigzag3": "M0,6 L3.33,2 L6.66,9.5 L11,3 L13.33,10 L16.66,2 L20,6",
    "zigzag4": "M0.7,1.3 L19.5,0.2 L0.2,9.5 L19.8,11.2",
    "rounded1": "M0.5,6 C2,1 5,1 4,6 C3,11 6,11 7,6 C8,1 11,1 10,6 C9,11 12,11 13,6 C14,1 17,1 16,6 C15,11 18,11 19.5,6",
    "rounded2": "M1,6 C1,1 8,1 8,6 C8,11 2,11 2,6 C2,2 12,2 12,6 C12,10 6,10 6,6 C6,1 16,1 16,6 C16,11 10,11 10,6 C10,2 19,2 19,6",
    "rounded3": "M1,6 C1,1 8,1 8,6 C8,11 1,11 1,6 C1,2 9,2 9,6 C9,10 2,10 2,6 C2,3 11,3 11,6 C11,9 4,9 4,6 C4,2 13,2 13,6 C13,10 6,10 6,6 C6,1 15,1 15,6 C15,11 8,11 8,6 C8,2 17,2 17,6 C17,10 10,10 10,6 C10,1 19,1 19,6 C19,11 12,11 12,6",
    "hatched1": "M0.5,6 L18.5,4 L2,8 L19,5 L1,7 L19.5,3 L0.8,9 L19,2 L1.2,10 L18.8,1.5 L0.5,10.5 L19.2,2.5 L1,9.5 L18.5,3.5 L1.5,8.5 L19,4.5 L0.8,7.5 L18.2,5.5 L2,6.5 L19.5,6",
    "hatched2": "M0.5,6 L19.5,5.2 L1,6.8 L19,5.5 L0.8,6.5 L19.2,5.8 L0.5,6.2 L19.5,5 L1.2,7 L18.8,5.1 L0.6,6.9 L19.4,5.3 L1,6.7 L19,5.6 L0.7,6.4 L19.3,5.7 L0.5,6.3 L19.5,4.8 L1.5,7.2 L19,6",
}

ICON_WRAPPER = '''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="none" stroke="#000000" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      {paths}
    </svg>
'''

LINE_WRAPPER = '''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 12" preserveAspectRatio="none">
        <path d="{paths}" fill="none" stroke="black" stroke-width="0.25"/>
    </svg>'''


def to_base64(wrapper, paths: str) -> str:
    wrapped = wrapper.format(paths=paths)
    cleaned = "".join(wrapped.splitlines()).strip()
    svg_bytes = cleaned.encode('utf-8')
    b64_string = base64.b64encode(svg_bytes).decode('utf-8')
    return f'url("data:image/svg+xml;base64,{b64_string}")'

def to_escaped__for_human(wrapper, paths: str) -> str:
    wrapped = wrapper.format(paths=paths)
    cleaned = "".join(wrapped.splitlines()).strip().replace('"', "'")
    cleaned = cleaned.replace('#', '%23')
    cleaned = cleaned.replace('<', '%3C')
    cleaned = cleaned.replace('>', '%3E')
    return f'url("data:image/svg+xml,{cleaned}")'

def to_escaped(wrapper, paths: str) -> str:
    wrapped = wrapper.format(paths=paths)
    cleaned = "".join(wrapped.splitlines()).strip().replace('"', "'")
    svg_clean = quote_for_svg(cleaned)
    return f'url("data:image/svg+xml,{svg_clean}")'


SVG_ICONS = dict(
    **{name: to_escaped__for_human(ICON_WRAPPER, path) for name, path in RAW_SVGS_ICONS.items()},
    **{name: to_escaped__for_human(LINE_WRAPPER, path) for name, path in RAW_SVGS_LINES.items()}
)
