import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Fay Yu · 俞云扉",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def image_to_b64(path: Path) -> str:
    """将图片转为 base64 字符串"""
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower().replace(".", "")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64,{b64}"

def load_photos():
    """加载 photos/ 文件夹中的摄影作品"""
    photos_dir = Path(__file__).parent / "photos"
    supported = {".jpg", ".jpeg", ".png", ".webp"}
    photos = []
    if photos_dir.exists():
        for f in sorted(photos_dir.iterdir()):
            if f.suffix.lower() in supported and f.name != ".gitkeep":
                src = image_to_b64(f)
                if src:
                    photos.append({"name": f.stem, "src": src})
    return photos

def build_gallery(photos):
    """构建摄影画廊 HTML"""
    if not photos:
        return "".join([
            '<div class="photo-slot" data-label="即将上传"></div>'
            for _ in range(6)
        ])
    slots = "".join([
        '<div class="photo-slot"><img src="{src}" alt="{name}"></div>'.format(**p)
        for p in photos[:6]
    ])
    for _ in range(max(0, 6 - len(photos))):
        slots += '<div class="photo-slot" data-label="即将上传"></div>'
    return slots

# ── 加载个人照片 ──
portrait_path = Path(__file__).parent / "portrait" / "portrait.jpg"
# 也支持 png/webp，自动查找
if not portrait_path.exists():
    for ext in [".png", ".webp", ".jpeg"]:
        candidate = Path(__file__).parent / "portrait" / f"portrait{ext}"
        if candidate.exists():
            portrait_path = candidate
            break

portrait_src = image_to_b64(portrait_path)

# ── 加载摄影作品 ──
photos = load_photos()
gallery = build_gallery(photos)

# ── 读取 HTML 模板 ──
template_path = Path(__file__).parent / "template.html"
html_template = template_path.read_text(encoding="utf-8")

# ── 注入动态内容（用 replace，避免 f-string 花括号转义问题）──
final_html = (
    html_template
    .replace("GALLERY_PLACEHOLDER", gallery)
    .replace("PORTRAIT_PLACEHOLDER", portrait_src)
)

st.markdown(final_html, unsafe_allow_html=True)
