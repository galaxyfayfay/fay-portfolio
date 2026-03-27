import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from pathlib import Path

st.set_page_config(
    page_title="Fay Yu · 俞云扉",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Load photos from /photos folder ──
def load_photos():
    photos_dir = Path(__file__).parent / "photos"
    supported = {".jpg", ".jpeg", ".png", ".webp"}
    photos = []
    if photos_dir.exists():
        for f in sorted(photos_dir.iterdir()):
            if f.suffix.lower() in supported:
                with open(f, "rb") as img:
                    b64 = base64.b64encode(img.read()).decode()
                ext = f.suffix.lower().replace(".", "")
                mime = "jpeg" if ext in ("jpg", "jpeg") else ext
                photos.append({
                    "name": f.stem,
                    "src": f"data:image/{mime};base64,{b64}"
                })
    return photos

photos = load_photos()

# Build photo slots HTML
def build_photo_gallery(photos):
    if not photos:
        slots = ""
        for i in range(6):
            slots += f'''
            <div class="photo-slot" data-label="即将上传">
            </div>'''
        return slots
    
    slots = ""
    for p in photos[:6]:
        slots += f'''
        <div class="photo-slot">
          <img src="{p["src"]}" alt="{p["name"]}">
        </div>'''
    # pad remaining slots
    for i in range(max(0, 6 - len(photos))):
        slots += '<div class="photo-slot" data-label="即将上传"></div>'
    return slots

gallery_html = build_photo_gallery(photos)

# ── Full HTML/CSS/JS portfolio ──
html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+SC:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}

:root {{
  --ink: #0e1912;
  --deep: #172a1d;
  --forest: #1f3625;
  --gold: #c9a96e;
  --gold-light: #dfc28a;
  --cream: #f3ead9;
  --mist: #b8c8b2;
}}

body {{
  background: var(--ink);
  color: var(--cream);
  font-family: 'Noto Serif SC', serif;
  overflow-x: hidden;
  cursor: none;
}}

/* Grain */
body::after {{
  content:'';
  position:fixed;
  inset:0;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
  pointer-events:none;
  z-index:9000;
}}

/* Cursor */
.cur {{ position:fixed; width:7px; height:7px; background:var(--gold); border-radius:50%; pointer-events:none; z-index:9999; transform:translate(-50%,-50%); }}
.cur-ring {{ position:fixed; width:30px; height:30px; border:1px solid rgba(201,169,110,.35); border-radius:50%; pointer-events:none; z-index:9998; transform:translate(-50%,-50%); transition:all .16s cubic-bezier(.25,.46,.45,.94); }}
.cur-ring.on {{ width:48px; height:48px; border-color:var(--gold); }}

/* Nav */
nav {{
  position:fixed; top:0; left:0; right:0; z-index:1000;
  padding:26px 60px;
  display:flex; justify-content:space-between; align-items:center;
  background:linear-gradient(to bottom,rgba(14,25,18,.92) 0%,transparent 100%);
}}
.nav-logo {{ font-family:'Cormorant Garamond',serif; font-size:1rem; letter-spacing:.18em; color:var(--gold); text-decoration:none; font-weight:300; }}
.nav-links {{ display:flex; gap:38px; list-style:none; }}
.nav-links a {{ color:var(--mist); text-decoration:none; font-size:.7rem; letter-spacing:.22em; text-transform:uppercase; font-family:'EB Garamond',serif; transition:color .25s; }}
.nav-links a:hover {{ color:var(--gold-light); }}

/* Hero */
#hero {{
  min-height:100vh;
  display:flex; align-items:center;
  padding:120px 60px 80px;
  position:relative; overflow:hidden;
}}
.hero-bg {{
  position:absolute; inset:0;
  background:
    radial-gradient(ellipse 55% 65% at 72% 48%, rgba(50,85,60,.16) 0%, transparent 60%),
    radial-gradient(ellipse 35% 45% at 18% 78%, rgba(201,169,110,.05) 0%, transparent 50%),
    linear-gradient(140deg,#0e1912 0%,#111d16 50%,#0e1912 100%);
}}
.hero-bg::before {{
  content:'';
  position:absolute; right:9%; top:12%; width:1px; height:68%;
  background:linear-gradient(to bottom,transparent,rgba(201,169,110,.25) 30%,rgba(201,169,110,.1) 70%,transparent);
  animation:breathe 7s ease-in-out infinite;
}}
.hero-bg::after {{
  content:'';
  position:absolute; right:14%; top:22%; width:1px; height:46%;
  background:linear-gradient(to bottom,transparent,rgba(201,169,110,.1) 50%,transparent);
  animation:breathe 10s ease-in-out infinite reverse;
}}
@keyframes breathe {{ 0%,100%{{opacity:.4}} 50%{{opacity:1}} }}

.hero-content {{ position:relative; z-index:1; max-width:880px; }}

.hero-eyebrow {{
  font-family:'EB Garamond',serif;
  font-size:.68rem; letter-spacing:.38em; text-transform:uppercase;
  color:var(--gold); margin-bottom:28px;
  display:flex; align-items:center; gap:14px;
  opacity:0; animation:fadeUp 1s .3s ease forwards;
}}
.hero-eyebrow::before {{ content:''; width:36px; height:1px; background:var(--gold); }}

.hero-name-zh {{
  font-family:'Noto Serif SC',serif;
  font-size:clamp(1.1rem,2.2vw,1.6rem);
  font-weight:300; letter-spacing:.14em;
  color:rgba(243,234,217,.45);
  opacity:0; animation:fadeUp 1.2s .5s ease forwards;
  margin-bottom:6px;
}}
.hero-name-en {{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(4.8rem,10.5vw,9.5rem);
  font-weight:300; font-style:italic;
  color:var(--cream); line-height:.88;
  letter-spacing:-.01em;
  opacity:0; animation:fadeUp 1.2s .65s ease forwards;
  margin-bottom:44px;
}}
.hero-desc {{
  font-size:.98rem; line-height:1.95;
  color:rgba(243,234,217,.55);
  font-weight:300; max-width:480px;
  opacity:0; animation:fadeUp 1.2s .85s ease forwards;
  margin-bottom:48px;
}}
.hero-tags {{
  display:flex; gap:10px; flex-wrap:wrap;
  opacity:0; animation:fadeUp 1.2s 1.05s ease forwards;
}}
.tag {{
  padding:6px 16px;
  border:1px solid rgba(201,169,110,.28);
  font-size:.68rem; letter-spacing:.14em; text-transform:uppercase;
  color:var(--gold); font-family:'EB Garamond',serif;
  transition:all .3s;
}}
.tag:hover {{ background:rgba(201,169,110,.07); border-color:var(--gold); }}

.hero-scroll {{
  position:absolute; bottom:38px; left:60px;
  display:flex; align-items:center; gap:12px;
  color:rgba(243,234,217,.28); font-size:.62rem;
  letter-spacing:.28em; text-transform:uppercase;
  font-family:'EB Garamond',serif;
  opacity:0; animation:fadeUp 1s 1.5s ease forwards;
}}
.scroll-line {{ width:56px; height:1px; background:rgba(243,234,217,.15); position:relative; overflow:hidden; }}
.scroll-line::after {{
  content:''; position:absolute; top:0; left:-100%; width:100%; height:100%;
  background:var(--gold);
  animation:slide 2.2s ease-in-out infinite;
}}
@keyframes slide {{ 0%{{left:-100%}} 100%{{left:100%}} }}
@keyframes fadeUp {{
  from {{ opacity:0; transform:translateY(22px); }}
  to {{ opacity:1; transform:translateY(0); }}
}}

/* Divider */
.divider {{ height:1px; background:linear-gradient(to right,transparent,rgba(201,169,110,.18),transparent); }}

/* Section label */
.section-label {{
  font-family:'EB Garamond',serif;
  font-size:.66rem; letter-spacing:.38em; text-transform:uppercase;
  color:var(--gold); display:flex; align-items:center; gap:14px;
  margin-bottom:60px;
}}
.section-label::before {{ content:''; width:28px; height:1px; background:var(--gold); }}

/* About */
#about {{ padding:130px 60px; background:linear-gradient(to bottom,var(--ink),var(--deep)); }}
.about-grid {{ display:grid; grid-template-columns:1fr 1.2fr; gap:90px; align-items:start; }}

.about-photo-frame {{ position:relative; }}
.about-photo-wrap {{
  width:100%; aspect-ratio:3/4;
  background:var(--forest);
  overflow:hidden;
}}
.about-photo-wrap img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.about-photo-wrap::before {{
  content:'Yu';
  position:absolute; inset:0;
  display:flex; align-items:center; justify-content:center;
  font-family:'Cormorant Garamond',serif;
  font-size:7rem; font-weight:300;
  color:rgba(201,169,110,.08);
}}
.about-photo-frame::before {{
  content:''; position:absolute; top:-10px; left:-10px;
  width:52px; height:52px;
  border-top:1px solid var(--gold); border-left:1px solid var(--gold);
  pointer-events:none;
}}
.about-photo-frame::after {{
  content:''; position:absolute; bottom:-10px; right:-10px;
  width:52px; height:52px;
  border-bottom:1px solid var(--gold); border-right:1px solid var(--gold);
  pointer-events:none;
}}

.about-text h2 {{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2.2rem,4.5vw,3.6rem);
  font-weight:300; line-height:1.12;
  color:var(--cream); margin-bottom:32px;
}}
.about-text h2 em {{ font-style:italic; color:var(--gold-light); }}
.about-text p {{
  font-size:.95rem; line-height:2.1;
  color:rgba(243,234,217,.58); font-weight:300;
  margin-bottom:18px;
}}

.about-stats {{
  display:grid; grid-template-columns:1fr 1fr; gap:28px;
  margin-top:48px; padding-top:44px;
  border-top:1px solid rgba(201,169,110,.12);
}}
.stat-num {{
  font-family:'Cormorant Garamond',serif;
  font-size:2.6rem; font-weight:300;
  color:var(--gold-light); line-height:1; margin-bottom:6px;
}}
.stat-label {{
  font-size:.68rem; letter-spacing:.14em; text-transform:uppercase;
  color:rgba(243,234,217,.35); font-family:'EB Garamond',serif;
}}

/* Experience */
#experience {{ padding:130px 60px; background:var(--deep); }}
.exp-timeline {{ position:relative; padding-left:38px; }}
.exp-timeline::before {{
  content:''; position:absolute; left:0; top:10px; bottom:10px; width:1px;
  background:linear-gradient(to bottom,var(--gold),rgba(201,169,110,.15) 70%,transparent);
}}
.exp-item {{
  position:relative; margin-bottom:64px;
  opacity:0; transform:translateX(-18px);
  transition:all .65s cubic-bezier(.25,.46,.45,.94);
}}
.exp-item.vis {{ opacity:1; transform:translateX(0); }}
.exp-dot {{
  position:absolute; left:-42px; top:9px;
  width:8px; height:8px;
  border:1px solid var(--gold); border-radius:50%;
  background:var(--deep); transition:all .3s;
}}
.exp-item:hover .exp-dot {{ background:var(--gold); box-shadow:0 0 10px rgba(201,169,110,.4); }}
.exp-meta {{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; flex-wrap:wrap; gap:6px; }}
.exp-company {{ font-family:'Noto Serif SC',serif; font-size:1.05rem; color:var(--cream); font-weight:400; }}
.exp-date {{ font-family:'EB Garamond',serif; font-size:.78rem; color:var(--gold); letter-spacing:.1em; }}
.exp-role {{ font-family:'EB Garamond',serif; font-size:.82rem; color:var(--gold-light); font-style:italic; margin-bottom:18px; }}
.exp-highlights {{ display:flex; flex-direction:column; gap:10px; }}
.exp-hl {{
  display:flex; gap:12px;
  font-size:.84rem; color:rgba(243,234,217,.52);
  font-family:'Noto Serif SC',serif; line-height:1.85; font-weight:300;
}}
.exp-hl::before {{ content:'◆'; font-size:.38rem; color:var(--gold); margin-top:8px; flex-shrink:0; }}

/* Education */
#education {{
  padding:130px 60px;
  background:linear-gradient(135deg,var(--ink) 0%,var(--deep) 50%,#101b14 100%);
  position:relative; overflow:hidden;
}}
#education::before {{
  content:'EDU'; position:absolute; right:-1%; top:50%;
  transform:translateY(-50%);
  font-family:'Cormorant Garamond',serif;
  font-size:19vw; font-weight:300;
  color:rgba(201,169,110,.022); pointer-events:none;
}}
.edu-cards {{ display:grid; grid-template-columns:1fr 1fr; gap:28px; }}
.edu-card {{
  border:1px solid rgba(201,169,110,.13);
  padding:44px; position:relative; overflow:hidden;
  transition:all .45s ease;
  opacity:0; transform:translateY(26px);
}}
.edu-card.vis {{ opacity:1; transform:translateY(0); }}
.edu-card:hover {{ border-color:rgba(201,169,110,.38); background:rgba(201,169,110,.025); }}
.edu-badge {{
  font-family:'Cormorant Garamond',serif;
  font-size:2.8rem; font-weight:300;
  color:rgba(201,169,110,.18); line-height:1; margin-bottom:22px;
}}
.edu-school {{ font-family:'Noto Serif SC',serif; font-size:1.1rem; color:var(--cream); margin-bottom:6px; }}
.edu-degree {{ font-family:'EB Garamond',serif; font-size:.82rem; color:var(--gold-light); font-style:italic; margin-bottom:18px; }}
.edu-period {{ font-family:'EB Garamond',serif; font-size:.68rem; letter-spacing:.2em; color:rgba(243,234,217,.28); text-transform:uppercase; margin-bottom:20px; }}
.edu-detail {{ font-size:.8rem; line-height:1.9; color:rgba(243,234,217,.42); font-family:'Noto Serif SC',serif; font-weight:300; }}

/* Projects */
#projects {{ padding:130px 60px; background:var(--deep); }}
.project-grid {{ display:grid; grid-template-columns:1.35fr 1fr; gap:22px; }}
.project-card {{
  position:relative; overflow:hidden; cursor:pointer;
  opacity:0; transform:translateY(18px);
  transition:opacity .65s ease,transform .65s ease;
}}
.project-card.vis {{ opacity:1; transform:translateY(0); }}
.project-inner {{
  height:100%; min-height:300px;
  position:relative; padding:48px 44px;
  border:1px solid rgba(201,169,110,.1);
  transition:border-color .45s ease;
  display:flex; flex-direction:column; justify-content:flex-end;
}}
.project-card:hover .project-inner {{ border-color:rgba(201,169,110,.32); }}
.project-inner::before {{
  content:''; position:absolute; inset:0;
  background:linear-gradient(to top,rgba(14,25,18,.88) 30%,rgba(14,25,18,.28) 100%);
}}
.project-bg-text {{
  position:absolute; top:22px; right:22px;
  font-family:'Cormorant Garamond',serif;
  font-size:4.5rem; font-weight:300;
  color:rgba(201,169,110,.07); line-height:1; z-index:0;
}}
.project-content {{ position:relative; z-index:1; }}
.project-num {{ font-family:'Cormorant Garamond',serif; font-size:.76rem; color:var(--gold); letter-spacing:.16em; margin-bottom:14px; }}
.project-title {{ font-family:'Noto Serif SC',serif; font-size:1.22rem; color:var(--cream); margin-bottom:10px; font-weight:400; line-height:1.4; }}
.project-desc {{ font-size:.8rem; color:rgba(243,234,217,.48); line-height:1.88; font-family:'Noto Serif SC',serif; font-weight:300; margin-bottom:22px; }}
.project-link {{
  display:inline-flex; align-items:center; gap:8px;
  font-family:'EB Garamond',serif; font-size:.72rem;
  letter-spacing:.2em; text-transform:uppercase;
  color:var(--gold); text-decoration:none; transition:gap .3s;
}}
.project-link:hover {{ gap:14px; }}
.project-link::after {{ content:'→'; }}

/* Photography */
#photography {{ padding:130px 60px; background:var(--ink); }}
.photo-intro {{ max-width:520px; margin-bottom:72px; }}
.photo-intro p {{ font-size:.95rem; line-height:2.05; color:rgba(243,234,217,.48); font-weight:300; }}
.photo-gallery {{ display:grid; grid-template-columns:repeat(3,1fr); gap:3px; }}
.photo-slot {{
  aspect-ratio:4/5; background:var(--forest);
  position:relative; overflow:hidden;
  border:1px solid rgba(201,169,110,.07);
  transition:border-color .45s ease; cursor:pointer;
}}
.photo-slot:nth-child(2) {{ aspect-ratio:4/6; }}
.photo-slot:hover {{ border-color:rgba(201,169,110,.28); }}
.photo-slot::before {{
  content:attr(data-label);
  position:absolute; inset:0;
  display:flex; align-items:center; justify-content:center;
  font-family:'Cormorant Garamond',serif;
  font-size:.72rem; letter-spacing:.28em; text-transform:uppercase;
  color:rgba(201,169,110,.25); transition:color .3s;
}}
.photo-slot:hover::before {{ color:rgba(201,169,110,.55); }}
.photo-slot img {{ width:100%; height:100%; object-fit:cover; display:block; transition:transform .75s cubic-bezier(.25,.46,.45,.94); }}
.photo-slot:hover img {{ transform:scale(1.04); }}

/* Skills */
#skills {{ padding:130px 60px; background:linear-gradient(180deg,var(--deep),var(--ink)); }}
.skills-layout {{ display:grid; grid-template-columns:1fr 1fr; gap:76px; align-items:start; }}
.skill-group {{ margin-bottom:44px; }}
.skill-group-title {{
  font-family:'EB Garamond',serif; font-size:.67rem;
  letter-spacing:.28em; text-transform:uppercase;
  color:var(--gold); margin-bottom:22px;
  padding-bottom:10px; border-bottom:1px solid rgba(201,169,110,.13);
}}
.skill-items {{ display:flex; flex-wrap:wrap; gap:7px; }}
.skill-item {{
  padding:6px 16px; font-size:.76rem;
  font-family:'Noto Serif SC',serif;
  color:rgba(243,234,217,.55);
  border:1px solid rgba(243,234,217,.1);
  transition:all .28s; font-weight:300;
}}
.skill-item:hover {{ color:var(--gold-light); border-color:rgba(201,169,110,.38); background:rgba(201,169,110,.04); }}

.lang-list {{ display:flex; flex-direction:column; gap:18px; }}
.lang-name {{ display:flex; justify-content:space-between; margin-bottom:7px; font-size:.8rem; color:rgba(243,234,217,.65); font-family:'Noto Serif SC',serif; }}
.lang-bar {{ height:1px; background:rgba(243,234,217,.07); position:relative; overflow:hidden; }}
.lang-fill {{
  position:absolute; top:0; left:0; bottom:0;
  background:linear-gradient(to right,var(--gold),var(--gold-light));
  width:0; transition:width 1.5s cubic-bezier(.25,.46,.45,.94);
}}
.lang-bar.anim .lang-fill {{ width:var(--pct); }}

/* Contact */
#contact {{ padding:130px 60px 72px; background:var(--ink); position:relative; overflow:hidden; }}
.contact-ghost {{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(3rem,8vw,7rem); font-weight:300;
  color:rgba(243,234,217,.055); margin-bottom:72px;
  line-height:1; pointer-events:none;
}}
.contact-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:72px; align-items:end; }}
.contact-left h3 {{ font-family:'Cormorant Garamond',serif; font-size:2.3rem; font-weight:300; color:var(--cream); margin-bottom:18px; }}
.contact-left p {{ font-size:.9rem; line-height:1.95; color:rgba(243,234,217,.42); font-family:'Noto Serif SC',serif; font-weight:300; max-width:380px; }}
.contact-links {{ display:flex; flex-direction:column; gap:22px; align-items:flex-end; }}
.contact-link {{ display:flex; align-items:center; gap:12px; color:rgba(243,234,217,.45); text-decoration:none; font-family:'EB Garamond',serif; font-size:.96rem; letter-spacing:.04em; transition:color .28s; }}
.contact-link:hover {{ color:var(--gold-light); }}
.contact-link span {{ font-size:.62rem; letter-spacing:.22em; text-transform:uppercase; color:var(--gold); opacity:.68; }}
.footer-bottom {{
  margin-top:88px; display:flex; justify-content:space-between; align-items:center;
  padding-top:28px; border-top:1px solid rgba(243,234,217,.05);
}}
.footer-sig {{ font-family:'Cormorant Garamond',serif; font-size:.95rem; font-style:italic; color:rgba(243,234,217,.18); }}
.footer-copy {{ font-size:.64rem; letter-spacing:.14em; color:rgba(243,234,217,.14); font-family:'EB Garamond',serif; text-transform:uppercase; }}

/* Orbs */
.orb {{ position:fixed; border-radius:50%; filter:blur(72px); pointer-events:none; z-index:0; }}
.orb-1 {{ width:380px; height:380px; background:rgba(50,85,60,.11); top:-8%; right:-4%; animation:orbf 14s ease-in-out infinite; }}
.orb-2 {{ width:280px; height:280px; background:rgba(201,169,110,.045); bottom:18%; left:-7%; animation:orbf 18s ease-in-out infinite reverse; }}
@keyframes orbf {{
  0%,100%{{transform:translate(0,0) scale(1)}}
  33%{{transform:translate(26px,-18px) scale(1.04)}}
  66%{{transform:translate(-18px,26px) scale(.96)}}
}}

/* Responsive */
@media (max-width:860px) {{
  nav {{ padding:22px 24px; }}
  .nav-links {{ gap:20px; }}
  #hero,#about,#experience,#education,#projects,#photography,#skills,#contact {{ padding-left:24px; padding-right:24px; }}
  .about-grid,.edu-cards,.project-grid,.skills-layout,.contact-grid {{ grid-template-columns:1fr; gap:44px; }}
  .contact-links {{ align-items:flex-start; }}
  .hero-scroll {{ left:24px; }}
  .photo-gallery {{ grid-template-columns:repeat(2,1fr); }}
}}
</style>
</head>
<body>

<div class="cur" id="cur"></div>
<div class="cur-ring" id="curRing"></div>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<!-- Nav -->
<nav>
  <a href="#hero" class="nav-logo">俞云扉</a>
  <ul class="nav-links">
    <li><a href="#about">关于</a></li>
    <li><a href="#experience">经历</a></li>
    <li><a href="#projects">项目</a></li>
    <li><a href="#photography">影像</a></li>
    <li><a href="#contact">联系</a></li>
  </ul>
</nav>

<!-- Hero -->
<section id="hero">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-eyebrow">Portfolio · 2026</div>
    <div class="hero-name-zh">俞云扉</div>
    <div class="hero-name-en">Fay Yu</div>
    <p class="hero-desc">
      携程集团产品助理，负责消费信贷产品「拿去花」的场景运营与增长。<br>
      今年秋天入读香港科技大学全球运营硕士项目。<br>
      做产品、写代码、偶尔拍照。
    </p>
    <div class="hero-tags">
      <span class="tag">Product Operations</span>
      <span class="tag">User Research</span>
      <span class="tag">A/B Testing</span>
      <span class="tag">Data Analysis</span>
      <span class="tag">Travel Tech</span>
    </div>
  </div>
  <div class="hero-scroll">
    <div class="scroll-line"></div>
    Scroll
  </div>
</section>

<div class="divider"></div>

<!-- About -->
<section id="about">
  <div class="about-grid">
    <div class="about-photo-frame">
      <div class="about-photo-wrap">
        <!-- 把你的照片放进 photos/ 文件夹，或者直接替换下面这行 -->
        <!-- <img src="photos/portrait.jpg" alt="Fay Yu"> -->
      </div>
    </div>
    <div class="about-text">
      <div class="section-label">About · 关于</div>
      <h2>产品、数据，<em>偶尔拍照</em></h2>
      <p>南京信息工程大学国际经济与贸易，专业前 5%，今年毕业。秋天去香港科大读全球运营硕士。</p>
      <p>在携程做「拿去花｜信用购」的产品运营——跑实验、做用研、看数据，也参与需求设计。入职以来主导或参与了多个提升转化率和用户体验的项目。</p>
      <p>自己从零独立开发了 AI 旅行规划 App Trip Planner，从写 PRD 到部署上线全流程，目前已迭代至 v11+。</p>
      <div class="about-stats">
        <div class="stat-item">
          <div class="stat-num">6万+</div>
          <div class="stat-label">用研问卷参与用户</div>
        </div>
        <div class="stat-item">
          <div class="stat-num">TOP 5%</div>
          <div class="stat-label">专业成绩排名</div>
        </div>
        <div class="stat-item">
          <div class="stat-num">v11+</div>
          <div class="stat-label">Trip Planner 迭代版本</div>
        </div>
        <div class="stat-item">
          <div class="stat-num">QS 47</div>
          <div class="stat-label">HKUST 世界排名</div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- Experience -->
<section id="experience">
  <div class="section-label">Experience · 实习经历</div>
  <div class="exp-timeline">

    <div class="exp-item">
      <div class="exp-dot"></div>
      <div class="exp-meta">
        <span class="exp-company">携程集团（上海）</span>
        <span class="exp-date">2025.07 — 至今</span>
      </div>
      <div class="exp-role">产品助理 · 金融事业部 · 拿去花｜信用购</div>
      <div class="exp-highlights">
        <div class="exp-hl">搭建 NPS/URS 用研体系，覆盖信分、金酒、贷后三大场景，10+ 份问卷、6万+ 用户参与，沉淀标准化问卷与流程</div>
        <div class="exp-hl">主导门票业务差异化获客策略，高峰时段引入差异化优惠券配置，前置激活人数提升约 4%</div>
        <div class="exp-hl">推进度假分期 A/B 实验，简化中期数展示，前置分期率提升 1.3%，组件渗透率提升 1%</div>
        <div class="exp-hl">参与「拿去花」前置实验设计与接口联调，实验带来 CR 提升 1%、渗透率提升约 3%</div>
        <div class="exp-hl">工单成本分析：按渠道/来源/类型分层拆解，推动页面与 IM 自助能力优化，H2 工单 CPO 环比下降 11%</div>
      </div>
    </div>

    <div class="exp-item">
      <div class="exp-dot"></div>
      <div class="exp-meta">
        <span class="exp-company">傲途乐梯（苏州）</span>
        <span class="exp-date">2024.12 — 2025.02</span>
      </div>
      <div class="exp-role">国际业务实习生 · 外贸部</div>
      <div class="exp-highlights">
        <div class="exp-hl">协同审查 4 份国际贸易合同，识别并规避 3 项潜在风险（涉及 HS 编码分类、强制认证缺失、付款条款），确保合规签约</div>
        <div class="exp-hl">重构 200+ SKU 品类映射表，优化物流排期与跨部门沟通机制，100% 按期交付，供链响应效率提升 5%</div>
      </div>
    </div>

    <div class="exp-item">
      <div class="exp-dot"></div>
      <div class="exp-meta">
        <span class="exp-company">深圳市朗华供应链</span>
        <span class="exp-date">2024.07 — 2024.08</span>
      </div>
      <div class="exp-role">供链外贸实习生 · 工业外贸事业部</div>
      <div class="exp-highlights">
        <div class="exp-hl">整合 3 家子公司供链数据，搭建可视化监控看板，提升管理层数据透明度</div>
        <div class="exp-hl">全英文独立对接 5 家海外客户，完成供链方案咨询与演示，客户满意度 100%</div>
      </div>
    </div>

  </div>
</section>

<div class="divider"></div>

<!-- Education -->
<section id="education">
  <div class="section-label">Education · 教育背景</div>
  <div class="edu-cards">
    <div class="edu-card">
      <div class="edu-badge">HKUST</div>
      <div class="edu-school">香港科技大学</div>
      <div class="edu-degree">MSc Global Operations · 全球运营硕士</div>
      <div class="edu-period">2026.08 — 2027.07 · QS 47 · 已录取</div>
      <div class="edu-detail">商学院全球运营项目，聚焦供应链管理、运营策略与国际商务。</div>
    </div>
    <div class="edu-card" style="transition-delay:.14s">
      <div class="edu-badge">NUIST</div>
      <div class="edu-school">南京信息工程大学（双一流）</div>
      <div class="edu-degree">BSc 国际经济与贸易</div>
      <div class="edu-period">2022.09 — 2026.06 · 专业排名 TOP 5%</div>
      <div class="edu-detail">
        核心课程：宏观经济学 96、微观经济学 94、国际结算 99、大数据与 AI 基础实践 96。<br>
        校国际交流协会主席；全国高校商务精英挑战总决赛一等奖；保诚（香港）国际商业体验计划优秀学员。
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- Projects -->
<section id="projects">
  <div class="section-label">Projects · 项目</div>
  <div class="project-grid">
    <div class="project-card">
      <div class="project-inner" style="background:linear-gradient(135deg,#1b3326 0%,#1f3a2a 100%)">
        <div class="project-bg-text">AI</div>
        <div class="project-content">
          <div class="project-num">001 · 2025—2026</div>
          <div class="project-title">Trip Planner · AI 旅行规划应用</div>
          <div class="project-desc">从写 PRD 到部署上线，独立完成的全流程产品项目。12 章节需求文档，基于 Python/Streamlit 构建，集成 DeepSeek、Overpass 与高德地图 API。核心功能：级联地点选择、分类景点推荐（支持单类刷新）、8km 地理聚类约束、HTML 地图导出。已迭代至 v11+，部署于 Streamlit Community Cloud。</div>
          <a class="project-link" href="https://ai-travel-planner-ysxzflexqdhmvty9ocshp3.streamlit.app/" target="_blank">访问应用</a>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:20px">
      <div class="project-card" style="transition-delay:.1s">
        <div class="project-inner" style="min-height:190px;background:linear-gradient(135deg,#182b1c,#1e3022)">
          <div class="project-bg-text" style="font-size:2.8rem">研</div>
          <div class="project-content">
            <div class="project-num">002 · 2023—2024</div>
            <div class="project-title">大学生创新创业项目</div>
            <div class="project-desc">老龄化背景下农村互助养老模式探索与优化</div>
          </div>
        </div>
      </div>
      <div class="project-card" style="transition-delay:.2s">
        <div class="project-inner" style="min-height:190px;background:linear-gradient(135deg,#1e301c,#1b2c1f)">
          <div class="project-bg-text" style="font-size:2.8rem">农</div>
          <div class="project-content">
            <div class="project-num">003 · 2022—2023</div>
            <div class="project-title">南京农业大学合作研究</div>
            <div class="project-desc">对外农业合作粮食安全战略能力评估</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- Photography -->
<section id="photography">
  <div class="section-label">Photography · 影像</div>
  <div class="photo-intro">
    <p>旅行时带相机，没有固定风格，就是记录。这里放一些觉得还不错的。</p>
  </div>
  <div class="photo-gallery">
    {gallery_html}
  </div>
</section>

<div class="divider"></div>

<!-- Skills -->
<section id="skills">
  <div class="section-label">Skills · 技能</div>
  <div class="skills-layout">
    <div>
      <div class="skill-group">
        <div class="skill-group-title">工具与技术</div>
        <div class="skill-items">
          <span class="skill-item">Python</span>
          <span class="skill-item">SQL</span>
          <span class="skill-item">Stata</span>
          <span class="skill-item">Figma</span>
          <span class="skill-item">XMind</span>
          <span class="skill-item">Visio</span>
          <span class="skill-item">Microsoft Office</span>
          <span class="skill-item">Vibe Coding</span>
          <span class="skill-item">AI Tools</span>
        </div>
      </div>
      <div class="skill-group">
        <div class="skill-group-title">专业能力</div>
        <div class="skill-items">
          <span class="skill-item">用户研究</span>
          <span class="skill-item">A/B 实验设计</span>
          <span class="skill-item">数据分析</span>
          <span class="skill-item">产品运营</span>
          <span class="skill-item">增长策略</span>
          <span class="skill-item">需求文档</span>
          <span class="skill-item">供应链管理</span>
        </div>
      </div>
    </div>
    <div>
      <div class="skill-group">
        <div class="skill-group-title">语言</div>
        <div class="lang-list">
          <div class="lang-item">
            <div class="lang-name"><span>普通话</span><span>母语</span></div>
            <div class="lang-bar"><div class="lang-fill" style="--pct:100%"></div></div>
          </div>
          <div class="lang-item">
            <div class="lang-name"><span>粤语</span><span>日常沟通</span></div>
            <div class="lang-bar"><div class="lang-fill" style="--pct:65%"></div></div>
          </div>
          <div class="lang-item">
            <div class="lang-name"><span>English</span><span>IELTS 7.5 · CET-6 584</span></div>
            <div class="lang-bar"><div class="lang-fill" style="--pct:88%"></div></div>
          </div>
          <div class="lang-item">
            <div class="lang-name"><span>Deutsch</span><span>基础</span></div>
            <div class="lang-bar"><div class="lang-fill" style="--pct:28%"></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- Contact -->
<section id="contact">
  <div class="contact-ghost">Say Hello</div>
  <div class="contact-grid">
    <div class="contact-left">
      <h3>联系我</h3>
      <p>实习合作、项目交流，或者只是聊聊，发邮件就行。</p>
    </div>
    <div class="contact-links">
      <a href="tel:+8615262676879" class="contact-link">
        <span>Tel</span>+86 152 6267 6879
      </a>
      <a href="mailto:galaxyfayfay0224@outlook.com" class="contact-link">
        <span>Mail</span>galaxyfayfay0224@outlook.com
      </a>
      <a href="https://ai-travel-planner-ysxzflexqdhmvty9ocshp3.streamlit.app/" target="_blank" class="contact-link">
        <span>Project</span>Trip Planner App ↗
      </a>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="footer-sig">俞云扉 · Fay Yu</div>
    <div class="footer-copy">© 2026 · Shanghai · HKUST Incoming</div>
  </div>
</section>

<script>
// Cursor
const cur = document.getElementById('cur');
const ring = document.getElementById('curRing');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{{
  mx=e.clientX; my=e.clientY;
  cur.style.left=mx+'px'; cur.style.top=my+'px';
}});
(function anim(){{
  rx+=(mx-rx)*.11; ry+=(my-ry)*.11;
  ring.style.left=rx+'px'; ring.style.top=ry+'px';
  requestAnimationFrame(anim);
}})();
document.querySelectorAll('a,button,.project-card,.photo-slot,.tag,.skill-item,.edu-card').forEach(el=>{{
  el.addEventListener('mouseenter',()=>ring.classList.add('on'));
  el.addEventListener('mouseleave',()=>ring.classList.remove('on'));
}});

// Scroll animations
const obs = new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{ if(e.isIntersecting) e.target.classList.add('vis'); }});
}},{{threshold:0.12}});
document.querySelectorAll('.exp-item,.edu-card,.project-card').forEach(el=>obs.observe(el));

// Language bars
const langObs = new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{
    if(e.isIntersecting) e.target.querySelectorAll('.lang-bar').forEach(b=>b.classList.add('anim'));
  }});
}},{{threshold:0.3}});
document.querySelectorAll('#skills').forEach(el=>langObs.observe(el));

// Nav active highlight
const navAs = document.querySelectorAll('.nav-links a');
const secObs = new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{
    if(e.isIntersecting){{
      navAs.forEach(a=>a.style.color = a.getAttribute('href')==='#'+e.target.id ? 'var(--gold-light)' : '');
    }}
  }});
}},{{threshold:0.35}});
document.querySelectorAll('section[id]').forEach(s=>secObs.observe(s));

// Hero parallax
window.addEventListener('scroll',()=>{{
  const c=document.querySelector('.hero-content');
  const s=window.scrollY;
  if(s<window.innerHeight){{
    c.style.transform=`translateY(${{s*.16}}px)`;
    c.style.opacity=1-s/(window.innerHeight*.75);
  }}
}});
</script>
</body>
</html>
"""

# Hide Streamlit chrome completely
st.markdown("""
<style>
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

components.html(html, height=10000, scrolling=False)
