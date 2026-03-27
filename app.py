import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Fay Yu · 俞云扉",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def image_to_b64(path):
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower().replace(".", "")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return "data:image/" + mime + ";base64," + b64

def load_photos():
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
    if not photos:
        return "".join([
            '<div class="photo-slot" data-label="即将上传"></div>'
            for _ in range(6)
        ])
    slots = ""
    for p in photos[:6]:
        slots += '<div class="photo-slot"><img src="' + p["src"] + '" alt="' + p["name"] + '"></div>'
    for _ in range(max(0, 6 - len(photos))):
        slots += '<div class="photo-slot" data-label="即将上传"></div>'
    return slots

# 加载个人照片
portrait_src = ""
portrait_dir = Path(__file__).parent / "portrait"
for ext in [".jpg", ".jpeg", ".png", ".webp"]:
    candidate = portrait_dir / ("portrait" + ext)
    if candidate.exists():
        portrait_src = image_to_b64(candidate)
        break

photos = load_photos()
gallery = build_gallery(photos)

# 用字符串拼接，完全不用 f-string
CSS = """
<style>
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton,
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] {
  display: none !important;
}
.main .block-container {
  padding: 0 !important;
  max-width: 100% !important;
  margin: 0 !important;
}
[data-testid="stAppViewContainer"] {
  padding: 0 !important;
  background: #0e1912 !important;
}
[data-testid="stVerticalBlock"] {
  gap: 0 !important;
  padding: 0 !important;
}
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+SC:wght@300;400;500&display=swap');
:root {
  --ink: #0e1912;
  --deep: #172a1d;
  --forest: #1f3625;
  --gold: #c9a96e;
  --gold-light: #dfc28a;
  --cream: #f3ead9;
  --mist: #b8c8b2;
}
#fay-root *, #fay-root *::before, #fay-root *::after {
  box-sizing: border-box;
}
#fay-root {
  background: var(--ink);
  color: var(--cream);
  font-family: 'Noto Serif SC', Georgia, serif;
  overflow-x: hidden;
  cursor: none;
  width: 100%;
  margin: 0;
  padding: 0;
  position: relative;
}
#fay-root::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9000;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.032'/%3E%3C/svg%3E");
}
#fay-cur {
  position: fixed;
  width: 7px;
  height: 7px;
  background: var(--gold);
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  transform: translate(-50%, -50%);
}
#fay-ring {
  position: fixed;
  width: 30px;
  height: 30px;
  border: 1px solid rgba(201,169,110,.35);
  border-radius: 50%;
  pointer-events: none;
  z-index: 9998;
  transform: translate(-50%, -50%);
  transition: width .16s, height .16s, border-color .16s;
}
#fay-ring.on {
  width: 48px;
  height: 48px;
  border-color: var(--gold);
}
.fay-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(72px);
  pointer-events: none;
}
.fay-orb-1 {
  width: 380px;
  height: 380px;
  background: rgba(50,85,60,.11);
  top: -8%;
  right: -4%;
  z-index: 0;
  animation: fay-orb 14s ease-in-out infinite;
}
.fay-orb-2 {
  width: 280px;
  height: 280px;
  background: rgba(201,169,110,.045);
  bottom: 18%;
  left: -7%;
  z-index: 0;
  animation: fay-orb 18s ease-in-out infinite reverse;
}
@keyframes fay-orb {
  0%,100% { transform: translate(0,0); }
  33% { transform: translate(24px,-16px); }
  66% { transform: translate(-16px,24px); }
}
#fay-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  padding: 26px 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(to bottom, rgba(14,25,18,.92), transparent);
}
.fay-logo {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1rem;
  letter-spacing: .18em;
  color: var(--gold);
  text-decoration: none;
  font-weight: 300;
}
.fay-nav-links {
  display: flex;
  gap: 36px;
  list-style: none;
  margin: 0;
  padding: 0;
}
.fay-nav-links a {
  color: var(--mist);
  text-decoration: none;
  font-size: .7rem;
  letter-spacing: .22em;
  text-transform: uppercase;
  font-family: 'EB Garamond', Georgia, serif;
  transition: color .25s;
}
.fay-nav-links a:hover { color: var(--gold-light); }
#fay-hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 120px 60px 80px;
  position: relative;
  overflow: hidden;
}
.fay-hero-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 55% 65% at 72% 48%, rgba(50,85,60,.16) 0%, transparent 60%),
    radial-gradient(ellipse 35% 45% at 18% 78%, rgba(201,169,110,.05) 0%, transparent 50%),
    linear-gradient(140deg, #0e1912 0%, #111d16 50%, #0e1912 100%);
}
.fay-hero-bg::before {
  content: '';
  position: absolute;
  right: 9%; top: 12%;
  width: 1px; height: 68%;
  background: linear-gradient(to bottom, transparent, rgba(201,169,110,.25) 30%, rgba(201,169,110,.1) 70%, transparent);
  animation: fay-breathe 7s ease-in-out infinite;
}
.fay-hero-bg::after {
  content: '';
  position: absolute;
  right: 14%; top: 22%;
  width: 1px; height: 46%;
  background: linear-gradient(to bottom, transparent, rgba(201,169,110,.1) 50%, transparent);
  animation: fay-breathe 10s ease-in-out infinite reverse;
}
@keyframes fay-breathe {
  0%,100% { opacity: .4; }
  50% { opacity: 1; }
}
.fay-hero-content {
  position: relative;
  z-index: 1;
  max-width: 880px;
}
.fay-eyebrow {
  font-family: 'EB Garamond', Georgia, serif;
  font-size: .68rem;
  letter-spacing: .38em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 28px;
  display: flex;
  align-items: center;
  gap: 14px;
  opacity: 0;
  animation: fay-up 1s .3s ease forwards;
}
.fay-eyebrow::before {
  content: '';
  width: 36px; height: 1px;
  background: var(--gold);
  flex-shrink: 0;
}
.fay-name-zh {
  font-family: 'Noto Serif SC', Georgia, serif;
  font-size: clamp(1.1rem, 2.2vw, 1.6rem);
  font-weight: 300;
  letter-spacing: .14em;
  color: rgba(243,234,217,.4);
  opacity: 0;
  animation: fay-up 1.2s .5s ease forwards;
  margin-bottom: 4px;
}
.fay-name-en {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(4.5rem, 10vw, 9rem);
  font-weight: 300;
  font-style: italic;
  color: var(--cream);
  line-height: .9;
  opacity: 0;
  animation: fay-up 1.2s .65s ease forwards;
  margin-bottom: 44px;
}
.fay-desc {
  font-size: .98rem;
  line-height: 2;
  color: rgba(243,234,217,.55);
  font-weight: 300;
  max-width: 480px;
  opacity: 0;
  animation: fay-up 1.2s .85s ease forwards;
  margin-bottom: 48px;
}
.fay-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  opacity: 0;
  animation: fay-up 1.2s 1.05s ease forwards;
}
.fay-tag {
  padding: 6px 16px;
  border: 1px solid rgba(201,169,110,.28);
  font-size: .68rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--gold);
  font-family: 'EB Garamond', serif;
  transition: all .3s;
}
.fay-tag:hover {
  background: rgba(201,169,110,.07);
  border-color: var(--gold);
}
.fay-scroll-hint {
  position: absolute;
  bottom: 38px; left: 60px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(243,234,217,.28);
  font-size: .62rem;
  letter-spacing: .28em;
  text-transform: uppercase;
  font-family: 'EB Garamond', serif;
  opacity: 0;
  animation: fay-up 1s 1.5s ease forwards;
}
.fay-scroll-line {
  width: 52px; height: 1px;
  background: rgba(243,234,217,.15);
  position: relative;
  overflow: hidden;
}
.fay-scroll-line::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: var(--gold);
  animation: fay-slide 2.2s ease-in-out infinite;
}
@keyframes fay-slide {
  0% { left: -100%; }
  100% { left: 100%; }
}
@keyframes fay-up {
  from { opacity: 0; transform: translateY(22px); }
  to { opacity: 1; transform: translateY(0); }
}
.fay-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(201,169,110,.18), transparent);
}
.fay-label {
  font-family: 'EB Garamond', Georgia, serif;
  font-size: .66rem;
  letter-spacing: .38em;
  text-transform: uppercase;
  color: var(--gold);
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 60px;
}
.fay-label::before {
  content: '';
  width: 28px; height: 1px;
  background: var(--gold);
  flex-shrink: 0;
}
#fay-about {
  padding: 130px 60px;
  background: linear-gradient(to bottom, var(--ink), var(--deep));
}
.fay-about-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 90px;
  align-items: start;
}
.fay-photo-frame { position: relative; }
.fay-photo-wrap {
  width: 100%;
  aspect-ratio: 3/4;
  background: var(--forest);
  overflow: hidden;
  position: relative;
}
.fay-photo-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  display: block;
  position: relative;
  z-index: 1;
}
.fay-photo-frame::before {
  content: '';
  position: absolute;
  top: -10px; left: -10px;
  width: 52px; height: 52px;
  border-top: 1px solid var(--gold);
  border-left: 1px solid var(--gold);
  pointer-events: none;
  z-index: 2;
}
.fay-photo-frame::after {
  content: '';
  position: absolute;
  bottom: -10px; right: -10px;
  width: 52px; height: 52px;
  border-bottom: 1px solid var(--gold);
  border-right: 1px solid var(--gold);
  pointer-events: none;
  z-index: 2;
}
.fay-about-text h2 {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(2rem, 4vw, 3.4rem);
  font-weight: 300;
  line-height: 1.15;
  color: var(--cream);
  margin-bottom: 32px;
}
.fay-about-text h2 em {
  font-style: italic;
  color: var(--gold-light);
}
.fay-about-text p {
  font-size: .95rem;
  line-height: 2.1;
  color: rgba(243,234,217,.58);
  font-weight: 300;
  margin-bottom: 18px;
}
.fay-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  margin-top: 48px;
  padding-top: 44px;
  border-top: 1px solid rgba(201,169,110,.12);
}
.fay-stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.5rem;
  font-weight: 300;
  color: var(--gold-light);
  line-height: 1;
  margin-bottom: 6px;
}
.fay-stat-label {
  font-size: .66rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: rgba(243,234,217,.35);
  font-family: 'EB Garamond', serif;
}
#fay-exp {
  padding: 130px 60px;
  background: var(--deep);
}
.fay-timeline {
  position: relative;
  padding-left: 38px;
}
.fay-timeline::before {
  content: '';
  position: absolute;
  left: 0; top: 10px; bottom: 10px;
  width: 1px;
  background: linear-gradient(to bottom, var(--gold), rgba(201,169,110,.15) 70%, transparent);
}
.fay-exp-item {
  position: relative;
  margin-bottom: 64px;
  opacity: 0;
  transform: translateX(-18px);
  transition: opacity .65s ease, transform .65s ease;
}
.fay-exp-item.vis { opacity: 1; transform: translateX(0); }
.fay-exp-dot {
  position: absolute;
  left: -42px; top: 9px;
  width: 8px; height: 8px;
  border: 1px solid var(--gold);
  border-radius: 50%;
  background: var(--deep);
  transition: all .3s;
}
.fay-exp-item:hover .fay-exp-dot {
  background: var(--gold);
  box-shadow: 0 0 10px rgba(201,169,110,.4);
}
.fay-exp-meta {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 6px;
  flex-wrap: wrap;
  gap: 6px;
}
.fay-exp-co {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.05rem;
  color: var(--cream);
  font-weight: 400;
}
.fay-exp-date {
  font-family: 'EB Garamond', serif;
  font-size: .78rem;
  color: var(--gold);
  letter-spacing: .1em;
}
.fay-exp-role {
  font-family: 'EB Garamond', serif;
  font-size: .82rem;
  color: var(--gold-light);
  font-style: italic;
  margin-bottom: 18px;
}
.fay-exp-hls {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.fay-hl {
  display: flex;
  gap: 12px;
  font-size: .84rem;
  color: rgba(243,234,217,.52);
  font-family: 'Noto Serif SC', serif;
  line-height: 1.85;
  font-weight: 300;
}
.fay-hl::before {
  content: '◆';
  font-size: .38rem;
  color: var(--gold);
  margin-top: 8px;
  flex-shrink: 0;
}
#fay-edu {
  padding: 130px 60px;
  background: linear-gradient(135deg, var(--ink), var(--deep) 50%, #101b14);
  position: relative;
  overflow: hidden;
}
#fay-edu::before {
  content: 'EDU';
  position: absolute;
  right: -1%; top: 50%;
  transform: translateY(-50%);
  font-family: 'Cormorant Garamond', serif;
  font-size: 19vw;
  font-weight: 300;
  color: rgba(201,169,110,.022);
  pointer-events: none;
}
.fay-edu-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}
.fay-edu-card {
  border: 1px solid rgba(201,169,110,.13);
  padding: 44px;
  opacity: 0;
  transform: translateY(26px);
  transition: opacity .6s ease, transform .6s ease, border-color .45s, background .45s;
}
.fay-edu-card.vis { opacity: 1; transform: translateY(0); }
.fay-edu-card:hover {
  border-color: rgba(201,169,110,.38);
  background: rgba(201,169,110,.025);
}
.fay-edu-badge {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.8rem;
  font-weight: 300;
  color: rgba(201,169,110,.18);
  line-height: 1;
  margin-bottom: 22px;
}
.fay-edu-school {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.1rem;
  color: var(--cream);
  margin-bottom: 6px;
}
.fay-edu-degree {
  font-family: 'EB Garamond', serif;
  font-size: .82rem;
  color: var(--gold-light);
  font-style: italic;
  margin-bottom: 18px;
}
.fay-edu-period {
  font-family: 'EB Garamond', serif;
  font-size: .68rem;
  letter-spacing: .2em;
  color: rgba(243,234,217,.28);
  text-transform: uppercase;
  margin-bottom: 20px;
}
.fay-edu-detail {
  font-size: .8rem;
  line-height: 1.9;
  color: rgba(243,234,217,.42);
  font-family: 'Noto Serif SC', serif;
  font-weight: 300;
}
#fay-proj {
  padding: 130px 60px;
  background: var(--deep);
}
.fay-proj-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 22px;
}
.fay-proj-card {
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(18px);
  transition: opacity .65s ease, transform .65s ease;
}
.fay-proj-card.vis { opacity: 1; transform: translateY(0); }
.fay-proj-inner {
  height: 100%;
  min-height: 300px;
  position: relative;
  padding: 48px 44px;
  border: 1px solid rgba(201,169,110,.1);
  transition: border-color .45s;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.fay-proj-card:hover .fay-proj-inner { border-color: rgba(201,169,110,.32); }
.fay-proj-inner::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(14,25,18,.88) 30%, rgba(14,25,18,.28) 100%);
}
.fay-proj-bg {
  position: absolute;
  top: 22px; right: 22px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 4.5rem;
  font-weight: 300;
  color: rgba(201,169,110,.07);
  line-height: 1;
}
.fay-proj-content { position: relative; z-index: 1; }
.fay-proj-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: .76rem;
  color: var(--gold);
  letter-spacing: .16em;
  margin-bottom: 14px;
}
.fay-proj-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.2rem;
  color: var(--cream);
  margin-bottom: 10px;
  font-weight: 400;
  line-height: 1.4;
}
.fay-proj-desc {
  font-size: .8rem;
  color: rgba(243,234,217,.48);
  line-height: 1.88;
  font-family: 'Noto Serif SC', serif;
  font-weight: 300;
  margin-bottom: 22px;
}
.fay-proj-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: 'EB Garamond', serif;
  font-size: .72rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--gold);
  text-decoration: none;
  transition: gap .3s;
}
.fay-proj-link:hover { gap: 14px; }
.fay-proj-link::after { content: '→'; }
#fay-photo {
  padding: 130px 60px;
  background: var(--ink);
}
.fay-photo-intro {
  max-width: 520px;
  margin-bottom: 72px;
}
.fay-photo-intro p {
  font-size: .95rem;
  line-height: 2.05;
  color: rgba(243,234,217,.48);
  font-weight: 300;
}
.fay-gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3px;
}
.photo-slot {
  aspect-ratio: 4/5;
  background: var(--forest);
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(201,169,110,.07);
  transition: border-color .45s;
  cursor: pointer;
}
.photo-slot:nth-child(2) { aspect-ratio: 4/6; }
.photo-slot:hover { border-color: rgba(201,169,110,.28); }
.photo-slot::before {
  content: attr(data-label);
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Cormorant Garamond', serif;
  font-size: .72rem;
  letter-spacing: .28em;
  text-transform: uppercase;
  color: rgba(201,169,110,.25);
  transition: color .3s;
}
.photo-slot:hover::before { color: rgba(201,169,110,.55); }
.photo-slot img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  transition: transform .75s cubic-bezier(.25,.46,.45,.94);
  position: relative;
  z-index: 1;
}
.photo-slot:hover img { transform: scale(1.04); }
#fay-skills {
  padding: 130px 60px;
  background: linear-gradient(180deg, var(--deep), var(--ink));
}
.fay-skills-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 76px;
  align-items: start;
}
.fay-skill-group { margin-bottom: 44px; }
.fay-skill-group-title {
  font-family: 'EB Garamond', serif;
  font-size: .67rem;
  letter-spacing: .28em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 22px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(201,169,110,.13);
}
.fay-skill-items {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}
.fay-skill-item {
  padding: 6px 16px;
  font-size: .76rem;
  font-family: 'Noto Serif SC', serif;
  color: rgba(243,234,217,.55);
  border: 1px solid rgba(243,234,217,.1);
  transition: all .28s;
  font-weight: 300;
}
.fay-skill-item:hover {
  color: var(--gold-light);
  border-color: rgba(201,169,110,.38);
  background: rgba(201,169,110,.04);
}
.fay-lang-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.fay-lang-name {
  display: flex;
  justify-content: space-between;
  margin-bottom: 7px;
  font-size: .8rem;
  color: rgba(243,234,217,.65);
  font-family: 'Noto Serif SC', serif;
}
.fay-lang-bar {
  height: 1px;
  background: rgba(243,234,217,.07);
  position: relative;
  overflow: hidden;
}
.fay-lang-fill {
  position: absolute;
  top: 0; left: 0; bottom: 0;
  background: linear-gradient(to right, var(--gold), var(--gold-light));
  width: 0;
  transition: width 1.5s cubic-bezier(.25,.46,.45,.94);
}
.fay-lang-bar.anim .fay-lang-fill { width: var(--pct); }
#fay-contact {
  padding: 130px 60px 72px;
  background: var(--ink);
}
.fay-contact-ghost {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 300;
  color: rgba(243,234,217,.055);
  margin-bottom: 72px;
  line-height: 1;
  pointer-events: none;
}
.fay-contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 72px;
  align-items: end;
}
.fay-contact-left h3 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.3rem;
  font-weight: 300;
  color: var(--cream);
  margin-bottom: 18px;
}
.fay-contact-left p {
  font-size: .9rem;
  line-height: 1.95;
  color: rgba(243,234,217,.42);
  font-family: 'Noto Serif SC', serif;
  font-weight: 300;
  max-width: 380px;
}
.fay-contact-links {
  display: flex;
  flex-direction: column;
  gap: 22px;
  align-items: flex-end;
}
.fay-contact-link {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(243,234,217,.45);
  text-decoration: none;
  font-family: 'EB Garamond', serif;
  font-size: .96rem;
  transition: color .28s;
}
.fay-contact-link:hover { color: var(--gold-light); }
.fay-contact-link span {
  font-size: .62rem;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: var(--gold);
  opacity: .68;
}
.fay-footer {
  margin-top: 88px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 28px;
  border-top: 1px solid rgba(243,234,217,.05);
}
.fay-footer-sig {
  font-family: 'Cormorant Garamond', serif;
  font-size: .95rem;
  font-style: italic;
  color: rgba(243,234,217,.18);
}
.fay-footer-copy {
  font-size: .64rem;
  letter-spacing: .14em;
  color: rgba(243,234,217,.14);
  font-family: 'EB Garamond', serif;
  text-transform: uppercase;
}
@media (max-width: 860px) {
  #fay-nav { padding: 22px 24px; }
  .fay-nav-links { gap: 18px; }
  #fay-hero, #fay-about, #fay-exp, #fay-edu,
  #fay-proj, #fay-photo, #fay-skills, #fay-contact {
    padding-left: 24px;
    padding-right: 24px;
  }
  .fay-about-grid, .fay-edu-cards, .fay-proj-grid,
  .fay-skills-layout, .fay-contact-grid {
    grid-template-columns: 1fr;
    gap: 44px;
  }
  .fay-contact-links { align-items: flex-start; }
  .fay-scroll-hint { left: 24px; }
  .fay-gallery { grid-template-columns: repeat(2, 1fr); }
}
</style>
"""

HTML_TOP = """
<div id="fay-root">
<div id="fay-cur"></div>
<div id="fay-ring"></div>
<div class="fay-orb fay-orb-1"></div>
<div class="fay-orb fay-orb-2"></div>
<nav id="fay-nav">
  <a href="#fay-hero" class="fay-logo">俞云扉</a>
  <ul class="fay-nav-links">
    <li><a href="#fay-about">关于</a></li>
    <li><a href="#fay-exp">经历</a></li>
    <li><a href="#fay-proj">项目</a></li>
    <li><a href="#fay-photo">影像</a></li>
    <li><a href="#fay-contact">联系</a></li>
  </ul>
</nav>
<section id="fay-hero">
  <div class="fay-hero-bg"></div>
  <div class="fay-hero-content">
    <div class="fay-eyebrow">Portfolio · 2026</div>
    <div class="fay-name-zh">俞云扉</div>
    <div class="fay-name-en">Fay Yu</div>
    <p class="fay-desc">
      携程集团产品助理，负责消费信贷产品「拿去花」的场景运营与增长。<br>
      今年秋天入读香港科技大学全球运营硕士。<br>
      做产品、写代码、偶尔拍照。
    </p>
    <div class="fay-tags">
      <span class="fay-tag">Product Operations</span>
      <span class="fay-tag">User Research</span>
      <span class="fay-tag">A/B Testing</span>
      <span class="fay-tag">Data Analysis</span>
      <span class="fay-tag">Travel Tech</span>
    </div>
  </div>
  <div class="fay-scroll-hint">
    <div class="fay-scroll-line"></div>
    Scroll
  </div>
</section>
<div class="fay-divider"></div>
<section id="fay-about">
  <div class="fay-about-grid">
    <div class="fay-photo-frame">
      <div class="fay-photo-wrap">
"""

# 个人照片注入点
PORTRAIT_IMG = '<img src="' + portrait_src + '" alt="Fay Yu" style="' + ('' if portrait_src else 'display:none') + '">'

HTML_ABOUT = """
      </div>
    </div>
    <div class="fay-about-text">
      <div class="fay-label">About · 关于</div>
      <h2>产品、数据，<em>偶尔拍照</em></h2>
      <p>南京信息工程大学国际经济与贸易，专业前 5%，今年毕业。秋天去香港科大读全球运营硕士。</p>
      <p>在携程做「拿去花｜信用购」的产品运营——跑实验、做用研、看数据。入职以来主导或参与了多个提升转化率和用户体验的项目。</p>
      <p>自己从零独立开发了 AI 旅行规划 App Trip Planner，从写 PRD 到部署上线全流程，目前迭代至 v11+。</p>
      <div class="fay-stats">
        <div><div class="fay-stat-num">6万+</div><div class="fay-stat-label">用研问卷参与用户</div></div>
        <div><div class="fay-stat-num">TOP 5%</div><div class="fay-stat-label">专业成绩排名</div></div>
        <div><div class="fay-stat-num">v11+</div><div class="fay-stat-label">Trip Planner 迭代版本</div></div>
        <div><div class="fay-stat-num">QS 47</div><div class="fay-stat-label">HKUST 世界排名</div></div>
      </div>
    </div>
  </div>
</section>
<div class="fay-divider"></div>
<section id="fay-exp">
  <div class="fay-label">Experience · 实习经历</div>
  <div class="fay-timeline">
    <div class="fay-exp-item">
      <div class="fay-exp-dot"></div>
      <div class="fay-exp-meta">
        <span class="fay-exp-co">携程集团（上海）</span>
        <span class="fay-exp-date">2025.07 — 至今</span>
      </div>
      <div class="fay-exp-role">产品助理 · 金融事业部 · 拿去花｜信用购</div>
      <div class="fay-exp-hls">
        <div class="fay-hl">搭建 NPS/URS 用研体系，覆盖信分、金酒、贷后三大场景，10+ 份问卷、6万+ 用户参与，沉淀标准化问卷与迭代流程</div>
        <div class="fay-hl">主导门票业务差异化获客策略，高峰时段引入差异化优惠券配置，前置激活人数提升约 4%</div>
        <div class="fay-hl">推进度假分期 A/B 实验，简化中期数展示，前置分期率提升 1.3%，组件渗透率提升 1%</div>
        <div class="fay-hl">参与「拿去花」前置实验设计与接口联调，实验带来 CR 提升 1%、渗透率提升约 3%</div>
        <div class="fay-hl">工单成本分析：按渠道/来源/类型分层拆解，推动页面与 IM 自助能力优化，H2 工单 CPO 环比下降 11%</div>
      </div>
    </div>
    <div class="fay-exp-item">
      <div class="fay-exp-dot"></div>
      <div class="fay-exp-meta">
        <span class="fay-exp-co">傲途乐梯（苏州）</span>
        <span class="fay-exp-date">2024.12 — 2025.02</span>
      </div>
      <div class="fay-exp-role">国际业务实习生 · 外贸部</div>
      <div class="fay-exp-hls">
        <div class="fay-hl">协同审查 4 份国际贸易合同，识别并规避 3 项潜在风险（HS 编码分类、强制认证缺失、付款条款），确保合规签约</div>
        <div class="fay-hl">重构 200+ SKU 品类映射表，优化物流排期与跨部门协作机制，100% 按期交付，供链响应效率提升 5%</div>
      </div>
    </div>
    <div class="fay-exp-item">
      <div class="fay-exp-dot"></div>
      <div class="fay-exp-meta">
        <span class="fay-exp-co">深圳市朗华供应链</span>
        <span class="fay-exp-date">2024.07 — 2024.08</span>
      </div>
      <div class="fay-exp-role">供链外贸实习生 · 工业外贸事业部</div>
      <div class="fay-exp-hls">
        <div class="fay-hl">整合 3 家子公司供链数据，搭建可视化监控看板，提升管理层数据透明度与决策效率</div>
        <div class="fay-hl">全英文独立对接 5 家海外客户，完成供链方案咨询与演示汇报，客户满意度 100%</div>
      </div>
    </div>
  </div>
</section>
<div class="fay-divider"></div>
<section id="fay-edu">
  <div class="fay-label">Education · 教育背景</div>
  <div class="fay-edu-cards">
    <div class="fay-edu-card">
      <div class="fay-edu-badge">HKUST</div>
      <div class="fay-edu-school">香港科技大学</div>
      <div class="fay-edu-degree">MSc Global Operations · 全球运营硕士</div>
      <div class="fay-edu-period">2026.08 — 2027.07 · QS 47 · 已录取</div>
      <div class="fay-edu-detail">商学院全球运营项目，聚焦供应链管理、运营策略与国际商务。</div>
    </div>
    <div class="fay-edu-card" style="transition-delay:.14s">
      <div class="fay-edu-badge">NUIST</div>
      <div class="fay-edu-school">南京信息工程大学（双一流）</div>
      <div class="fay-edu-degree">BSc 国际经济与贸易</div>
      <div class="fay-edu-period">2022.09 — 2026.06 · 专业排名 TOP 5%</div>
      <div class="fay-edu-detail">
        核心课程：宏观经济学 96、微观经济学 94、国际结算 99、大数据与 AI 基础实践 96。<br>
        校国际交流协会主席；全国高校商务精英挑战总决赛一等奖；保诚（香港）国际商业体验计划优秀学员。
      </div>
    </div>
  </div>
</section>
<div class="fay-divider"></div>
<section id="fay-proj">
  <div class="fay-label">Projects · 项目</div>
  <div class="fay-proj-grid">
    <div class="fay-proj-card">
      <div class="fay-proj-inner" style="background:linear-gradient(135deg,#1b3326,#1f3a2a)">
        <div class="fay-proj-bg">AI</div>
        <div class="fay-proj-content">
          <div class="fay-proj-num">001 · 2025—2026</div>
          <div class="fay-proj-title">Trip Planner · AI 旅行规划应用</div>
          <div class="fay-proj-desc">从写 PRD 到部署上线，独立完成的全流程产品项目。12 章节需求文档，基于 Python/Streamlit 构建，集成 DeepSeek、Overpass 与高德地图 API。核心功能：级联地点选择、分类景点推荐、8km 地理聚类约束、HTML 地图导出。已迭代至 v11+，部署于 Streamlit Community Cloud。</div>
          <a class="fay-proj-link" href="https://ai-travel-planner-ysxzflexqdhmvty9ocshp3.streamlit.app/" target="_blank">访问应用</a>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:20px">
      <div class="fay-proj-card" style="transition-delay:.1s">
        <div class="fay-proj-inner" style="min-height:190px;background:linear-gradient(135deg,#182b1c,#1e3022)">
          <div class="fay-proj-bg" style="font-size:2.8rem">研</div>
          <div class="fay-proj-content">
            <div class="fay-proj-num">002 · 2023—2024</div>
            <div class="fay-proj-title">大学生创新创业项目</div>
            <div class="fay-proj-desc">老龄化背景下农村互助养老模式探索与优化</div>
          </div>
        </div>
      </div>
      <div class="fay-proj-card" style="transition-delay:.2s">
        <div class="fay-proj-inner" style="min-height:190px;background:linear-gradient(135deg,#1e301c,#1b2c1f)">
          <div class="fay-proj-bg" style="font-size:2.8rem">农</div>
          <div class="fay-proj-content">
            <div class="fay-proj-num">003 · 2022—2023</div>
            <div class="fay-proj-title">南京农业大学合作研究</div>
            <div class="fay-proj-desc">对外农业合作粮食安全战略能力评估</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<div class="fay-divider"></div>
<section id="fay-photo">
  <div class="fay-label">Photography · 影像</div>
  <div class="fay-photo-intro">
    <p>旅行时带相机，没有固定风格，就是记录。这里放一些觉得还不错的。</p>
  </div>
  <div class="fay-gallery">
"""

HTML_SKILLS = """
  </div>
</section>
<div class="fay-divider"></div>
<section id="fay-skills">
  <div class="fay-label">Skills · 技能</div>
  <div class="fay-skills-layout">
    <div>
      <div class="fay-skill-group">
        <div class="fay-skill-group-title">工具与技术</div>
        <div class="fay-skill-items">
          <span class="fay-skill-item">Python</span>
          <span class="fay-skill-item">SQL</span>
          <span class="fay-skill-item">Stata</span>
          <span class="fay-skill-item">Figma</span>
          <span class="fay-skill-item">XMind</span>
          <span class="fay-skill-item">Visio</span>
          <span class="fay-skill-item">Microsoft Office</span>
          <span class="fay-skill-item">Vibe Coding</span>
          <span class="fay-skill-item">AI Tools</span>
        </div>
      </div>
      <div class="fay-skill-group">
        <div class="fay-skill-group-title">专业能力</div>
        <div class="fay-skill-items">
          <span class="fay-skill-item">用户研究</span>
          <span class="fay-skill-item">A/B 实验设计</span>
          <span class="fay-skill-item">数据分析</span>
          <span class="fay-skill-item">产品运营</span>
          <span class="fay-skill-item">增长策略</span>
          <span class="fay-skill-item">需求文档</span>
          <span class="fay-skill-item">供应链管理</span>
        </div>
      </div>
    </div>
    <div>
      <div class="fay-skill-group">
        <div class="fay-skill-group-title">语言</div>
        <div class="fay-lang-list">
          <div>
            <div class="fay-lang-name"><span>普通话</span><span>母语</span></div>
            <div class="fay-lang-bar"><div class="fay-lang-fill" style="--pct:100%"></div></div>
          </div>
          <div>
            <div class="fay-lang-name"><span>粤语</span><span>日常沟通</span></div>
            <div class="fay-lang-bar"><div class="fay-lang-fill" style="--pct:65%"></div></div>
          </div>
          <div>
            <div class="fay-lang-name"><span>English</span><span>IELTS 7.5 · CET-6 584</span></div>
            <div class="fay-lang-bar"><div class="fay-lang-fill" style="--pct:88%"></div></div>
          </div>
          <div>
            <div class="fay-lang-name"><span>Deutsch</span><span>基础</span></div>
            <div class="fay-lang-bar"><div class="fay-lang-fill" style="--pct:28%"></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<div class="fay-divider"></div>
<section id="fay-contact">
  <div class="fay-contact-ghost">Say Hello</div>
  <div class="fay-contact-grid">
    <div class="fay-contact-left">
      <h3>联系我</h3>
      <p>实习合作、项目交流，或者只是聊聊，发邮件就行。</p>
    </div>
    <div class="fay-contact-links">
      <a href="tel:+8615262676879" class="fay-contact-link"><span>Tel</span>+86 152 6267 6879</a>
      <a href="mailto:galaxyfayfay0224@outlook.com" class="fay-contact-link"><span>Mail</span>galaxyfayfay0224@outlook.com</a>
      <a href="https://ai-travel-planner-ysxzflexqdhmvty9ocshp3.streamlit.app/" target="_blank" class="fay-contact-link"><span>Project</span>Trip Planner App ↗</a>
    </div>
  </div>
  <div class="fay-footer">
    <div class="fay-footer-sig">俞云扉 · Fay Yu</div>
    <div class="fay-footer-copy">© 2026 · Shanghai · HKUST Incoming</div>
  </div>
</section>
</div>
<script>
(function() {
  var cur = document.getElementById('fay-cur');
  var ring = document.getElementById('fay-ring');
  if (!cur || !ring) return;
  var mx=0,my=0,rx=0,ry=0;
  document.addEventListener('mousemove',function(e){
    mx=e.clientX;my=e.clientY;
    cur.style.left=mx+'px';cur.style.top=my+'px';
  });
  (function tick(){
    rx+=(mx-rx)*0.11;ry+=(my-ry)*0.11;
    ring.style.left=rx+'px';ring.style.top=ry+'px';
    requestAnimationFrame(tick);
  })();
  document.querySelectorAll('a,.fay-proj-card,.photo-slot,.fay-tag,.fay-skill-item,.fay-edu-card').forEach(function(el){
    el.addEventListener('mouseenter',function(){ring.classList.add('on');});
    el.addEventListener('mouseleave',function(){ring.classList.remove('on');});
  });
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){if(e.isIntersecting)e.target.classList.add('vis');});
  },{threshold:0.1});
  document.querySelectorAll('.fay-exp-item,.fay-edu-card,.fay-proj-card').forEach(function(el){obs.observe(el);});
  var sk=document.getElementById('fay-skills');
  if(sk){
    new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting)e.target.querySelectorAll('.fay-lang-bar').forEach(function(b){b.classList.add('anim');});
      });
    },{threshold:0.3}).observe(sk);
  }
  window.addEventListener('scroll',function(){
    var c=document.querySelector('.fay-hero-content');
    var s=window.scrollY;
    if(c&&s<window.innerHeight){
      c.style.transform='translateY('+(s*0.15)+'px)';
      c.style.opacity=Math.max(0,1-s/(window.innerHeight*0.75));
    }
  });
})();
</script>
"""

# 拼接最终 HTML，完全不用 f-string
final_html = CSS + HTML_TOP + PORTRAIT_IMG + HTML_ABOUT + gallery + HTML_SKILLS

st.markdown(final_html, unsafe_allow_html=True)
