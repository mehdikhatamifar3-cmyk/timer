import json
import streamlit as st
import streamlit.components.v1 as components

# Checked against JCU's published procedures on 23 November 2026.
# Classroom directions (names, stapled pages and seating) are local instructions.
# Suspected academic misconduct must be reported; no automatic two-strike
# dismissal rule is asserted here.
JCU_MISCONDUCT_URL = (
    "https://www.jcu.edu.au/policy/academic-governance/student-experience/"
    "student-academic-misconduct-procedure"
)
JCU_EXAM_URL = (
    "https://www.jcu.edu.au/policy/academic-governance/learning-and-teaching/"
    "examinations-procedure"
)
DEFAULT_INSTRUCTIONS = [
    (
        "Write your name first",
        "Before answering any questions, write your full name and student ID "
        "in the spaces provided on your quiz paper.",
    ),
    (
        "If you separate the pages",
        "If you separate the stapled pages, write your full name and student ID "
        "on EVERY page first. Hand in all pages together.",
    ),
    (
        "Spread out in the room",
        "Spread out and leave an empty seat between classmates wherever "
        "possible. Follow staff seating directions.",
    ),
    (
        "Permitted materials only",
        "On your desk: permitted materials only.\n"
        "Put bags away. Switch off and put away phones, watches and other "
        "unapproved devices.",
    ),
    (
        "Keep your eyes on your own paper",
        "Work independently.\nDo not look at another student's answers or "
        "show them your own. Do not talk or share materials.",
    ),
    (
        "Follow the supervisor's instructions",
        "Need help? Raise your hand.\nStart only when instructed. Stop writing "
        "immediately when told.\nHand in every page of your quiz.",
    ),
]
INSTRUCTION_VISUALS = [
    {"kind": "name", "label": "Name", "category": "IDENTIFICATION", "tip": "Name first. Answers second."},
    {"kind": "pages", "label": "Pages", "category": "KEEP YOUR WORK IDENTIFIABLE", "tip": "Separate pages = a name on every page."},
    {"kind": "seating", "label": "Seating", "category": "CHOOSE YOUR SEAT", "tip": "Give yourself and your classmates space."},
    {"kind": "desk", "label": "Desk", "category": "CLEAR YOUR DESK", "tip": "If you are unsure whether an item is allowed, ask first."},
    {"kind": "independent", "label": "Own work", "category": "WORK INDEPENDENTLY", "tip": "Your paper. Your answers. Your work."},
    {"kind": "hand", "label": "Staff", "category": "ASK FOR HELP", "tip": "Raise a hand and wait for the supervisor."},
]
INTEGRITY_MESSAGE = (
    "Looking at others' answers or other suspected cheating will be "
    "recorded and reported under JCU's Student Academic Misconduct Procedure. "
    "Follow any warning or direction immediately. A warning does not prevent "
    "reporting; penalties follow the University process."
)

st.set_page_config(
    page_title="ExamTimer Pro",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background:#07101f;}
.block-container {padding:1rem;max-width:1600px;}
[data-testid="stSidebar"] {background:#0b1730;border-right:2px solid #1d3561;}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] span {color:#fff!important;}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,[data-testid="stSidebar"] small {color:#d6e2f5!important;opacity:1!important;}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {font-weight:650!important;}
[data-testid="stSidebar"] input {color:#102038!important;background:#fff!important;-webkit-text-fill-color:#102038!important;opacity:1!important;font-weight:650!important;}
[data-testid="stSidebar"] input::placeholder {color:#607089!important;-webkit-text-fill-color:#607089!important;opacity:1!important;}
[data-testid="stSidebar"] input:disabled {color:#31445f!important;-webkit-text-fill-color:#31445f!important;background:#e9eef5!important;opacity:1!important;}
[data-testid="stSidebar"] textarea {color:#102038!important;background:#fff!important;-webkit-text-fill-color:#102038!important;}
[data-testid="stSidebar"] div[data-baseweb="select"]>div {background:#fff!important;border-color:#b9c7da!important;}
[data-testid="stSidebar"] div[data-baseweb="select"] span,[data-testid="stSidebar"] div[data-baseweb="select"] svg {color:#102038!important;fill:#102038!important;}
[data-testid="stSidebar"] [data-testid="stSlider"] div,[data-testid="stSidebar"] [data-testid="stSlider"] span {color:#fff!important;}
[data-testid="stSidebarCollapseButton"] button,[data-testid="stSidebarCollapseButton"] svg {color:#fff!important;fill:#fff!important;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("ExamTimer Pro")
    st.caption("Configure the instructions and timer, then launch the projector display.")
    title = st.text_input("Exam or subject title", "ME3512 Examination")
    subtitle = st.text_input("Subtitle", "Please manage your time carefully")

    st.subheader("Pre-quiz instructions")
    start_with_instructions = st.toggle("Open on instructions page", True)
    instruction_view = st.selectbox(
        "Instruction display", ["Presentation", "All instructions"]
    )
    instruction_autoplay = st.toggle("Auto-play instructions", False)
    instruction_interval = st.slider("Seconds per instruction", 8, 30, 14, 1)
    animate_instructions = st.toggle("Animate instructions", True)
    permitted_materials = st.text_area(
        "Permitted materials for this quiz",
        "Standard stationery. Calculators, notes and other materials only if "
        "expressly permitted for this quiz.",
        height=100,
        max_chars=600,
    )
    extra_comments_raw = st.text_area(
        "Extra comments (one per line)",
        "",
        height=100,
        max_chars=3000,
        help="These appear below the main instructions. Leave blank if not needed.",
    )
    instruction_font_size = st.slider("Instruction text size", 18, 32, 22, 1)
    instruction_cards = []
    with st.expander("Edit the six main instructions"):
        for index, (heading, default_text) in enumerate(DEFAULT_INSTRUCTIONS):
            text = st.text_area(
                heading, default_text, height=115,
                max_chars=1000, key=f"instruction_{index}",
            )
            instruction_cards.append({
                "title": heading, "text": text, **INSTRUCTION_VISUALS[index]
            })
    st.caption("Long comments receive extra reading time during auto-play. The final instruction stays on screen.")
    st.caption("Set sidebar options before starting. Changing them reloads the display.")

    st.subheader("Timing")
    reading_on = st.toggle("Include reading time", True)
    reading_minutes = st.number_input(
        "Reading time (minutes)", 0, 120, 10, 1,
        disabled=not reading_on,
    )
    c1, c2 = st.columns(2)
    with c1:
        hours = st.number_input("Exam hours", 0, 12, 1, 1)
    with c2:
        minutes = st.number_input("Extra minutes", 0, 59, 50, 5)

    st.subheader("Visual alerts")
    amber = st.slider("Amber below (%)", 10, 80, 50, 5)
    red = st.slider("Red below (%)", 1, 40, 20, 1)
    flash = st.slider("Flash below (%)", 1, 15, 5, 1)
    sound = st.toggle("Sound alerts", True)
    milestones_raw = st.text_input("Warnings at minutes remaining", "30, 15, 5, 1")
    end_message = st.text_input("End message", "TIME EXPIRED — STOP WRITING")

    st.subheader("Appearance")
    theme = st.selectbox(
        "Theme",
        ["Midnight", "Light", "Slate", "Ocean", "Forest", "High Contrast", "Warm Sand", "JCU Blue & Gold", "Engineering Graphite", "Examination White", "Lecture Blue"],
    )
    show_logo = st.toggle("Show subtle JCU shield", True)
    collapse_sidebar = st.toggle("Collapse sidebar when timer starts", True)

try:
    milestones = sorted(
        {int(item.strip()) for item in milestones_raw.split(",") if int(item.strip()) > 0},
        reverse=True,
    )
except ValueError:
    milestones = [30, 15, 5, 1]
    st.sidebar.warning("Use comma-separated whole numbers for warnings.")

exam_seconds = int(hours * 3600 + minutes * 60)
if exam_seconds <= 0:
    st.error("Set an exam duration greater than zero.")
    st.stop()

config = {
    "title": title,
    "subtitle": subtitle,
    "reading": int(reading_minutes * 60) if reading_on else 0,
    "exam": exam_seconds,
    "amber": amber,
    "red": red,
    "flash": flash,
    "sound": sound,
    "milestones": milestones,
    "endMessage": end_message,
    "theme": theme,
    "showLogo": show_logo,
    "collapseSidebar": collapse_sidebar,
    "logo": "https://www.jcu.edu.au/__data/assets/image/0017/2322521/JCU-Logo-Shield-RGB-copy.png",
    "startPage": "instructions" if start_with_instructions else "timer",
    "instructions": instruction_cards,
    "instructionFontSize": instruction_font_size,
    "instructionMode": "overview" if instruction_view == "All instructions" else "presentation",
    "instructionAutoplay": instruction_autoplay,
    "instructionInterval": instruction_interval,
    "animateInstructions": animate_instructions,
    "permittedMaterials": permitted_materials.strip(),
    "extraComments": [line.strip() for line in extra_comments_raw.splitlines() if line.strip()],
    "integrityMessage": INTEGRITY_MESSAGE,
}
config_json = json.dumps(config).replace("</", "<\\/")

html = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{
 --bg:#07101f;--panel:#101c31;--text:#f5f8ff;--muted:#aebbd1;
 --accent:#2ed47a;--track:#263653;--glow:#2ed47a66;
 --banner-bg:#f7fbff;--banner-text:#102038;--banner-border:#2ed47a;
 --button-text:#8799b2;--button-hover:#c7d5e8;--button-border:rgba(119,143,174,.20);--button-bg:rgba(18,34,56,.34);--primary-text:#9fc8b0;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;height:100%;overflow:hidden;font-family:Inter,Segoe UI,Arial,sans-serif;background:var(--bg);color:var(--text)}
body.light{--bg:#edf3fb;--panel:#fff;--text:#102038;--muted:#52637b;--track:#d5dfeb;--banner-bg:#102038;--banner-text:#fff;--button-text:#102038}
body.slate{--bg:#171a21;--panel:#242936;--text:#f7f8fb;--muted:#b8bfcc;--track:#3b4353;--banner-bg:#f7f8fb;--banner-text:#171a21}
body.ocean{--bg:#041b2d;--panel:#0a3048;--text:#f2fbff;--muted:#abd0df;--track:#1d526b;--banner-bg:#eefbff;--banner-text:#04243a}
body.forest{--bg:#071c16;--panel:#103128;--text:#f2fff9;--muted:#acd3c3;--track:#285848;--banner-bg:#f1fff8;--banner-text:#0a2b20}
body.contrast{--bg:#000;--panel:#111;--text:#fff;--muted:#fff;--track:#555;--banner-bg:#fff200;--banner-text:#000;--button-text:#fff}
body.sand{--bg:#f3ead8;--panel:#fffaf0;--text:#3a2a1e;--muted:#705b48;--track:#d7c4a5;--banner-bg:#342519;--banner-text:#fff8e9;--button-text:#3a2a1e}
body.jcu{--bg:#061b35;--panel:#0b315a;--text:#f7fbff;--muted:#b9cee0;--track:#285177;--banner-bg:#f4c542;--banner-text:#071b33;--button-text:#fff}
body.engineering{--bg:#111418;--panel:#242a31;--text:#f3f6f8;--muted:#aeb8c2;--track:#45505c;--banner-bg:#f3f6f8;--banner-text:#111418;--button-text:#f3f6f8}
body.examwhite{--bg:#f7f8fa;--panel:#fff;--text:#111827;--muted:#4b5563;--track:#d1d5db;--banner-bg:#111827;--banner-text:#fff;--button-text:#111827}
body.lecture{--bg:#071c33;--panel:#0d3458;--text:#f5fbff;--muted:#b8d4e8;--track:#28577d;--banner-bg:#f5fbff;--banner-text:#092744;--button-text:#fff}
.shell{height:100vh;min-height:0;padding:18px 24px;display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;background:radial-gradient(circle at 50% 42%,var(--glow),transparent 34%),var(--bg);transition:.4s}
.page-nav{display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:10px;margin:14px 0 8px}
.page-nav button{font:inherit;font-size:15px;font-weight:800;padding:9px 18px;border:1px solid var(--track);border-radius:999px;color:var(--muted);background:var(--panel);cursor:pointer}
.page-nav button.active{color:var(--text);border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.page-nav button:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.page-status{font-size:14px;color:var(--muted);font-variant-numeric:tabular-nums;padding:0 8px}
.instructions-page{min-height:0;display:flex;flex-direction:column;gap:12px;overflow:hidden;padding:8px 8px 12px}
.briefing-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;flex-shrink:0}
.briefing-label{display:flex;align-items:center;gap:10px;font-size:13px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}
.briefing-label::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--accent);box-shadow:0 0 14px var(--glow)}
.briefing-tools{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.briefing-tool,.nav-arrow,.step-link{font:inherit;cursor:pointer;border:1px solid var(--track);background:var(--panel);color:var(--muted);border-radius:12px;transition:background .2s,border-color .2s,transform .2s,color .2s}
.briefing-tool{padding:9px 13px;font-size:14px;font-weight:750}.briefing-tool.active,.briefing-tool.playing{border-color:var(--accent);color:var(--text);background:var(--panel);box-shadow:inset 0 0 0 1px var(--accent)}
.briefing-tool:hover,.nav-arrow:hover,.step-link:hover{color:var(--text);border-color:var(--accent);transform:translateY(-1px)}
.briefing-tool:focus-visible,.nav-arrow:focus-visible,.step-link:focus-visible,.instruction-card:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.spotlight{--slide-color:#73d7ff;--slide-ink:#00627e;--slide-rgb:115,215,255;position:relative;isolation:isolate;flex:1;min-height:0;display:grid;grid-template-columns:minmax(160px,.8fr) minmax(0,2fr);gap:clamp(20px,3vw,58px);align-items:center;padding:clamp(20px,3.1vw,56px);border:1px solid rgba(var(--slide-rgb),.36);border-radius:28px;background:linear-gradient(125deg,rgba(var(--slide-rgb),.12),transparent 65%),var(--panel);box-shadow:0 20px 60px #0002;overflow:hidden}
.spotlight::before{content:'';position:absolute;z-index:-1;left:-100px;top:-170px;width:430px;height:430px;border-radius:50%;background:radial-gradient(circle,rgba(var(--slide-rgb),.15),transparent 70%);pointer-events:none}
.spotlight.entering .spotlight-copy{animation:briefEnter .4s ease both}.spotlight.entering .spotlight-art{animation:briefEnter .5s ease both}
.spotlight-art{position:relative;width:100%;max-width:330px;aspect-ratio:1;max-height:100%;display:grid;place-items:center;justify-self:center;border:1px solid rgba(var(--slide-rgb),.18);border-radius:26px;background:linear-gradient(150deg,rgba(var(--slide-rgb),.12),transparent);color:var(--slide-color)}
.instruction-art{display:block;position:static;inset:auto;transform:none;filter:none;padding:0;width:100%;height:auto;max-height:100%;overflow:visible;color:inherit}
.spotlight-art .instruction-art{width:88%;max-width:285px;animation:briefFloat 6s ease-in-out infinite}
.spotlight-copy{min-width:0;min-height:0;max-height:100%;overflow-y:auto;overscroll-behavior:contain;scrollbar-color:rgba(var(--slide-rgb),.45) transparent;padding:3px 9px 3px 0}
.slide-kicker{font-size:clamp(12px,1.05vw,16px);font-weight:850;letter-spacing:2px;line-height:1.5;margin:0 0 12px;color:var(--slide-color)}
.slide-title{font-size:clamp(30px,3.65vw,66px);font-weight:900;line-height:1.08;letter-spacing:-1.4px;margin:0 0 20px;overflow-wrap:anywhere;text-wrap:balance}
.slide-copy{font-size:clamp(var(--instruction-font,22px),2.15vw,38px);line-height:1.48;margin:0;white-space:pre-line;overflow-wrap:anywhere;color:var(--text)}
.slide-copy strong,.card-copy strong{color:var(--slide-color);font-weight:850}
.slide-tip{display:inline-block;font-size:clamp(15px,1.25vw,21px);font-weight:750;line-height:1.4;margin:22px 0 0;padding:10px 14px;border-left:3px solid var(--slide-color);border-radius:0 10px 10px 0;background:rgba(var(--slide-rgb),.08);color:var(--muted);overflow-wrap:anywhere}
.slide-progress{position:absolute;bottom:0;left:0;right:0;height:5px;background:rgba(var(--slide-rgb),.10)}
.slide-progress-fill{display:block;width:100%;height:100%;background:var(--slide-color);transform:scaleX(0);transform-origin:left center;transition:transform .1s linear;box-shadow:0 0 15px rgba(var(--slide-rgb),.3)}
.instruction-navigator{display:flex;align-items:center;gap:12px;flex-shrink:0;min-width:0}
.nav-arrow{flex-shrink:0;width:44px;height:44px;font-size:24px;color:var(--text)}.nav-arrow:disabled{opacity:.3;cursor:default;transform:none}
.step-area{flex:1;min-width:0;text-align:center}.step-track{display:flex;align-items:center;justify-content:flex-start;gap:7px;overflow-x:auto;scrollbar-width:thin;padding:3px;max-width:max-content;margin:auto;max-height:64px}
.step-link{display:flex;align-items:center;gap:7px;white-space:nowrap;padding:9px 11px;font-size:13px;font-weight:700;flex-shrink:0}
.step-link.active{color:var(--text);border-color:var(--accent);background:var(--panel);box-shadow:inset 0 -2px 0 var(--accent)}
.step-digit{font-variant-numeric:tabular-nums;font-size:12px;font-weight:850;opacity:.8}
.auto-status{color:var(--muted);font-size:12px;line-height:1.3;margin-top:7px;min-height:16px}
.instruction-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px;flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;align-content:start;padding:3px 5px 12px;scrollbar-color:var(--track) var(--bg)}
.instruction-card{--slide-color:#73d7ff;--slide-ink:#00627e;--slide-rgb:115,215,255;appearance:none;font:inherit;color:var(--text);text-align:left;cursor:pointer;background:linear-gradient(125deg,rgba(var(--slide-rgb),.08),transparent 70%),var(--panel);border:1px solid var(--track);border-radius:20px;padding:20px;display:grid;grid-template-columns:54px minmax(0,1fr);gap:15px;align-items:start;box-shadow:0 6px 20px #0002;transition:transform .25s,border-color .25s,box-shadow .25s;animation:briefEnter .35s ease both;animation-delay:calc(var(--card-order,0)*35ms)}
.instruction-card:hover{transform:translateY(-3px);border-color:var(--slide-color);box-shadow:0 12px 30px #0003}.instruction-card.wide-card{grid-column:1/-1}
.card-icon{color:var(--slide-color);padding:5px;background:rgba(var(--slide-rgb),.09);border:1px solid rgba(var(--slide-rgb),.18);border-radius:14px}
.card-category{font-size:11px;font-weight:850;letter-spacing:1.4px;color:var(--slide-color);margin-bottom:6px;line-height:1.4}
.instruction-card h2{font-size:clamp(20px,1.7vw,28px);line-height:1.2;letter-spacing:-.3px;margin:0 0 10px;font-weight:850;overflow-wrap:anywhere}
.card-copy{font-size:var(--instruction-font,22px);line-height:1.45;margin:0;white-space:pre-line;overflow-wrap:anywhere}
.instruction-note{font-size:14px;color:var(--muted);margin:8px 0 10px}
.instructions-mode{--accent:#51c9ff;--glow:#51c9ff22}.instructions-mode .header-finish{display:none}
body.light .instructions-mode,body.sand .instructions-mode,body.examwhite .instructions-mode{--accent:#006797;--glow:#00679718}
body.light .slide-kicker,body.sand .slide-kicker,body.examwhite .slide-kicker,body.light .slide-copy strong,body.sand .slide-copy strong,body.examwhite .slide-copy strong,body.light .card-category,body.sand .card-category,body.examwhite .card-category,body.light .card-copy strong,body.sand .card-copy strong,body.examwhite .card-copy strong,body.light .card-icon,body.sand .card-icon,body.examwhite .card-icon,body.light .spotlight-art,body.sand .spotlight-art,body.examwhite .spotlight-art{color:var(--slide-ink)}
body.contrast .spotlight,body.contrast .instruction-card{background:#111;border-color:#fff}body.contrast .slide-copy strong,body.contrast .card-copy strong{color:#fff200}
@keyframes briefEnter{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes briefFloat{0%,100%{transform:translateY(0) rotate(-1deg)}50%{transform:translateY(-7px) rotate(1deg)}}
.no-instruction-motion .instructions-page *{animation:none!important;transition:none!important}
@media(prefers-reduced-motion:reduce){.instructions-page *,.instructions-page *::before{animation:none!important;transition:none!important}}
@media(max-width:1050px){.step-label{display:none}.step-link{min-width:34px;justify-content:center;padding:8px}.spotlight{grid-template-columns:minmax(130px,.65fr) minmax(0,2fr);gap:20px;padding:24px}.slide-title{font-size:clamp(28px,4vw,46px)}}
@media(max-width:800px){.instruction-grid{grid-template-columns:1fr}.page-status{width:100%;text-align:center}.instruction-card{padding:16px;grid-template-columns:42px minmax(0,1fr);gap:12px}.card-copy{font-size:clamp(18px,3.5vw,var(--instruction-font,22px))}.spotlight{grid-template-columns:minmax(0,1fr)}.spotlight-art{display:none}.slide-title{font-size:clamp(29px,5vw,42px)}.slide-copy{font-size:var(--instruction-font,22px)}.slide-kicker{font-size:12px}.slide-tip{font-size:15px;margin-top:17px}.briefing-toolbar{gap:8px}.briefing-tools{gap:5px}.briefing-tool{font-size:12px;padding:8px 10px}.briefing-label{font-size:11px}.instruction-navigator{gap:6px}.nav-arrow{width:34px;height:38px}.step-track{gap:4px}.step-link{padding:8px 6px;min-width:29px}.auto-status{font-size:11px}}
header{text-align:center;position:relative}.logo{position:absolute;left:6px;top:3px;height:62px;max-width:92px;object-fit:contain;opacity:.30;filter:saturate(.65);transition:.25s}
.title{font-size:clamp(27px,3vw,48px);font-weight:900}.subtitle{font-size:clamp(14px,1.4vw,22px);color:var(--muted);margin-top:5px}.header-finish{font-size:clamp(13px,1.15vw,18px);color:var(--muted);font-weight:750;margin-top:7px}
.stage{display:grid;place-items:center;position:relative;overflow:visible;min-height:0;padding:18px 30px}.timer{width:min(57vh,590px);height:min(57vh,590px);min-width:350px;min-height:350px;position:relative;display:grid;place-items:center;perspective:1000px;overflow:visible;margin:12px}
.disc{position:absolute;inset:8%;border-radius:50%;background:radial-gradient(circle at 50% 34%,rgba(255,255,255,.14),transparent 25%),var(--panel);box-shadow:0 38px 75px #0008,inset 0 8px 16px #fff1,inset 0 -22px 40px #0006;transform:rotateX(7deg)}
.timer>svg{position:absolute;inset:-9%;width:118%;height:118%;padding:9%;overflow:visible;transform:rotate(-90deg);filter:none}.track,.progress{fill:none;stroke-width:22}.track{stroke:var(--track)}.progress{stroke:var(--accent);stroke-linecap:round;transition:stroke .3s,stroke-width .45s,stroke-dashoffset .3s;filter:drop-shadow(0 0 8px var(--accent)) drop-shadow(0 0 15px var(--glow));animation:ringBreathe 8s ease-in-out infinite;will-change:filter}@keyframes ringBreathe{0%,100%{filter:drop-shadow(0 0 7px var(--accent)) drop-shadow(0 0 12px var(--glow))}50%{filter:drop-shadow(0 0 12px var(--accent)) drop-shadow(0 0 24px var(--glow))}}
.content{z-index:2;text-align:center}.phase{font-size:clamp(17px,1.7vw,25px);font-weight:900;letter-spacing:3px;color:var(--accent)}.clock{font-size:clamp(68px,8.5vw,135px);font-weight:950;letter-spacing:-5px;font-variant-numeric:tabular-nums;text-shadow:0 8px 26px #0007}.pct{font-size:clamp(16px,1.5vw,23px);color:var(--muted);font-weight:700}
.banner{position:absolute;z-index:4;width:min(92%,900px);padding:30px 38px;border:3px solid var(--banner-border);border-radius:24px;background:var(--banner-bg);color:var(--banner-text);text-align:center;font-size:clamp(28px,4vw,57px);font-weight:950;line-height:1.15;letter-spacing:.3px;box-shadow:0 25px 80px #000b,0 0 35px var(--glow);opacity:0;transform:scale(.85);pointer-events:none;transition:.25s}.banner.show{opacity:1;transform:scale(1)}.markers{position:absolute;inset:0;z-index:1;pointer-events:none}.marker{position:absolute;width:9px;height:9px;border-radius:50%;background:var(--muted);box-shadow:0 0 0 3px var(--panel);opacity:.7}.m75{left:50%;top:3%;transform:translateX(-50%)}.m50{right:3%;top:50%;transform:translateY(-50%)}.m25{left:50%;bottom:3%;transform:translateX(-50%)}.m10{left:9%;top:69%}.end-screen{position:absolute;inset:0;z-index:8;display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;background:radial-gradient(circle,#75131d,#260207 72%);color:#fff;opacity:0;pointer-events:none;transition:.35s}.end-screen.show{opacity:1;pointer-events:auto}.end-main{font-size:clamp(58px,8vw,132px);font-weight:950;letter-spacing:2px}.end-sub{font-size:clamp(30px,4vw,68px);font-weight:900;margin-top:12px}.end-line{width:min(72%,900px);height:5px;background:#fff;margin:24px 0;border-radius:4px}
footer{text-align:center;position:relative;z-index:10;padding:4px 0 8px;overflow:visible}.meta{color:var(--muted);margin:0 0 10px}.controls{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:9px;opacity:1!important;visibility:visible!important;pointer-events:auto!important;transform:none!important;filter:none!important;position:relative;z-index:12}.controls:hover,.controls:focus-within,.controls.controls-visible{opacity:1!important;visibility:visible!important}.controls button{padding:11px 17px;border-radius:12px;border:1px solid var(--button-border);background:var(--button-bg);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);color:var(--button-text);font-size:15px;font-weight:750;cursor:pointer;box-shadow:none;opacity:1!important;visibility:visible!important;transition:color .22s ease,background .22s ease,border-color .22s ease,transform .22s ease}.controls button:hover,.controls button:focus-visible{color:var(--button-hover);background:rgba(84,112,148,.22);border-color:rgba(151,176,207,.46);transform:translateY(-1px);outline:none}.controls .primary{background:rgba(46,212,122,.10);color:#93bfa5;border-color:rgba(82,177,121,.25)}.controls .primary:hover{background:rgba(46,212,122,.18);color:#c8ead5;border-color:rgba(82,177,121,.45)}body.light .controls button,body.sand .controls button,body.examwhite .controls button{background:rgba(35,58,84,.07);color:#66778d;border-color:rgba(52,76,105,.17)}body.light .controls button:hover,body.sand .controls button:hover,body.examwhite .controls button:hover{background:rgba(35,58,84,.13);color:#2f435b;border-color:rgba(52,76,105,.32)}.controls button:disabled{opacity:.35;cursor:not-allowed;filter:grayscale(.45);box-shadow:none}.controls .lock-active{background:rgba(255,176,32,.14);color:#c9a761;border-color:rgba(255,196,91,.32)}.flash{animation:flash .8s infinite}@keyframes flash{50%{filter:brightness(1.6)}}
.shell:fullscreen{padding:clamp(18px,2vw,42px)}.shell:fullscreen .stage{padding:20px 34px}.shell:fullscreen .timer{width:min(60vh,68vw);height:min(60vh,68vw);max-width:760px;max-height:760px;margin:12px}.shell:fullscreen .clock{font-size:clamp(100px,12vw,210px)}.shell:fullscreen .phase{font-size:clamp(24px,2.5vw,40px)}.shell:fullscreen .pct{font-size:clamp(20px,2vw,32px)}.shell:fullscreen .title{font-size:clamp(38px,4vw,72px)}.shell:fullscreen .subtitle{font-size:clamp(18px,1.8vw,30px)}.shell:fullscreen .logo{height:clamp(65px,8vh,105px);max-width:140px;opacity:.25}.shell:fullscreen .banner{font-size:clamp(42px,5vw,82px);padding:42px}
@media(max-width:650px){.shell{padding:10px}.stage{padding:12px}.timer{min-width:280px;min-height:280px;width:min(50vh,82vw);height:min(50vh,82vw);margin:8px}.logo{height:42px}.clock{letter-spacing:-2px}.banner{padding:22px 18px}}
</style>
</head>
<body>
<div class="shell" id="shell">
<header><img class="logo" id="logo"><div class="title" id="title"></div><div class="subtitle" id="subtitle"></div><div class="header-finish" id="headerFinish">Finish time: --:--</div></header>
<nav class="page-nav" aria-label="Display pages"><button type="button" id="instructionsTab" aria-controls="instructionsPage" aria-pressed="false">Before the quiz</button><button type="button" id="timerTab" aria-controls="timerPage" aria-pressed="false">Timer</button><span class="page-status" id="pageStatus" role="timer" aria-live="off"></span></nav>
<main class="instructions-page" id="instructionsPage" aria-label="Before the quiz" tabindex="0" hidden>
<div class="briefing-toolbar">
<div class="briefing-label" id="slideCount" aria-live="polite" aria-atomic="true"></div>
<div class="briefing-tools" aria-label="Instruction presentation controls"><button class="briefing-tool" id="presentMode" aria-pressed="true">Presentation</button><button class="briefing-tool" id="overviewMode" aria-pressed="false">All instructions</button><button class="briefing-tool" id="autoToggle" aria-pressed="false">▶ Auto-play</button></div>
</div>
<section class="spotlight" id="instructionSpotlight" aria-roledescription="slide" aria-label="Quiz instruction">
<div class="spotlight-art" id="slideArt" aria-hidden="true"></div>
<div class="spotlight-copy" id="slideCopy"><p class="slide-kicker" id="slideCategory"></p><h2 class="slide-title" id="slideTitle"></h2><p class="slide-copy" id="slideBody"></p><p class="slide-tip" id="slideTip"></p></div>
<div class="slide-progress" aria-hidden="true"><span class="slide-progress-fill" id="slideProgress"></span></div>
</section>
<div class="instruction-grid" id="instructionGrid" aria-label="All quiz instructions" hidden></div>
<div class="instruction-navigator" id="instructionNavigator"><button class="nav-arrow" id="previousInstruction" aria-label="Previous instruction">←</button><div class="step-area"><div class="step-track" id="slideSteps" aria-label="Go to an instruction"></div><div class="auto-status" id="autoStatus" aria-live="off"></div></div><button class="nav-arrow" id="nextInstruction" aria-label="Next instruction">→</button></div>
</main>
<main class="stage" id="timerPage" aria-label="Countdown timer" hidden>
<div class="timer"><div class="disc"></div><div class="markers"><span class="marker m75" title="75%"></span><span class="marker m50" title="50%"></span><span class="marker m25" title="25%"></span><span class="marker m10" title="10%"></span></div><svg viewBox="0 0 420 420"><circle class="track" cx="210" cy="210" r="180"/><circle class="progress" id="ring" cx="210" cy="210" r="180"/></svg><div class="content"><div class="phase" id="phase">READY</div><div class="clock" id="clock"></div><div class="pct" id="pct"></div></div></div>
<div class="banner" id="banner"></div><div class="end-screen" id="endScreen"><div class="end-line"></div><div class="end-main">TIME EXPIRED</div><div class="end-sub">STOP WRITING NOW</div><div class="end-line"></div></div>
</main>
<footer><div id="instructionFooter"><div class="instruction-note">Approved assessment adjustments still apply. Do not begin until instructed.</div><div class="controls"><button class="primary" id="showTimer">▶ Show timer</button><button id="instructionsFull">⛶ Full Screen</button></div></div><div id="timerFooter" hidden><div class="meta"><span id="elapsed"></span></div><div class="controls"><button class="primary" id="start">▶ Start</button><button id="pause">Ⅱ Pause</button><button id="plus">+ 1 min</button><button id="plus5">+ 5 min</button><button id="plus10">+ 10 min</button><button id="minus">− 1 min</button><button id="reset">↺ Reset</button><button id="warn15">⚠ 15 min</button><button id="warn5">⚠ 5 min</button><button id="stopmsg">■ Stop Writing</button><button id="lock">🔒 Lock Controls</button><button id="full">⛶ Full Screen</button></div></div></footer>
</div>
<script>
const c=__CONFIG__,$=id=>document.getElementById(id);
const themeClasses={Light:'light',Slate:'slate',Ocean:'ocean',Forest:'forest','High Contrast':'contrast','Warm Sand':'sand','JCU Blue & Gold':'jcu','Engineering Graphite':'engineering','Examination White':'examwhite','Lecture Blue':'lecture'};
if(themeClasses[c.theme])document.body.classList.add(themeClasses[c.theme]);
$('title').textContent=c.title;$('subtitle').textContent=c.subtitle;
if(c.showLogo){$('logo').src=c.logo}else{$('logo').style.display='none'}
const L=2*Math.PI*180;$('ring').style.strokeDasharray=L;
let phase=c.reading?'reading':'exam',total=c.reading||c.exam,left=total,elapsed=0,running=false,ended=false,target=0,timer=null,said=new Set(),bannerTimer=null,locked=false;
let currentPage=c.startPage;
document.documentElement.style.setProperty('--instruction-font',c.instructionFontSize+'px');
const prefersReducedMotion=typeof window.matchMedia==='function'&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!c.animateInstructions||prefersReducedMotion)$('shell').classList.add('no-instruction-motion');
let instructionMode=c.instructionMode,slideIndex=0,autoplay=false,autoTimer=null,autoTarget=0,autoDuration=0;
const instructionSlides=[],stepButtons=[],overviewCards=[];
const slidePalettes=[
 {color:'#73d7ff',ink:'#00627e',rgb:'115,215,255'},
 {color:'#c6adff',ink:'#6540a8',rgb:'198,173,255'},
 {color:'#79e6bb',ink:'#096644',rgb:'121,230,187'},
 {color:'#a7c5ff',ink:'#254c9b',rgb:'167,197,255'},
 {color:'#ffa4ad',ink:'#a22e39',rgb:'255,164,173'},
 {color:'#ffda8b',ink:'#78500a',rgb:'255,218,139'},
];
// Decorative vector illustrations are fixed app content; user text stays text.
const artPaths={
 name:'<rect x="67" y="32" width="166" height="200" rx="18" fill="currentColor" fill-opacity=".06"/><path d="M96 81h106M96 139h106M96 186h73" opacity=".4"/><text x="96" y="65" fill="currentColor" stroke="none" font-size="13" font-weight="800" font-family="Arial,sans-serif">FULL NAME</text><text x="96" y="121" fill="currentColor" stroke="none" font-size="13" font-weight="800" font-family="Arial,sans-serif">STUDENT ID</text><path d="m107 188 17-20 8 14 20-26"/><circle cx="226" cy="207" r="31" fill="var(--panel)"/><path d="m212 207 10 10 19-21"/>',
 pages:'<rect x="36" y="54" width="106" height="151" rx="13" transform="rotate(-12 89 130)" fill="var(--panel)"/><rect x="165" y="54" width="106" height="151" rx="13" transform="rotate(12 218 130)" fill="var(--panel)"/><rect x="98" y="37" width="111" height="166" rx="13" fill="var(--panel)"/><path d="M117 70h73M117 99h73M117 128h55M117 157h45" opacity=".5"/><path d="M54 89h32M220 89h32"/><circle cx="153" cy="211" r="28" fill="var(--panel)"/><path d="m139 211 10 10 20-21"/>',
 seating:'<g fill="currentColor" fill-opacity=".10"><rect x="42" y="66" width="54" height="43" rx="9"/><rect x="204" y="66" width="54" height="43" rx="9"/><rect x="42" y="171" width="54" height="43" rx="9"/><rect x="204" y="171" width="54" height="43" rx="9"/></g><g opacity=".32" stroke-dasharray="5 7"><rect x="123" y="66" width="54" height="43" rx="9"/><rect x="123" y="171" width="54" height="43" rx="9"/></g><circle cx="69" cy="43" r="13" fill="currentColor"/><circle cx="231" cy="148" r="13" fill="currentColor"/><path d="M110 137h80m-70-10-10 10 10 10m60-20 10 10-10 10"/>',
 desk:'<rect x="30" y="116" width="210" height="31" rx="9" fill="currentColor" fill-opacity=".10"/><path d="M49 147v70m172-70v70M70 69h74v47H70zM97 69v47m61-37 14-14 25 25-14 14z"/><circle cx="113" cy="180" r="28"/><path d="m99 180 10 10 19-20"/><g opacity=".65"><rect x="254" y="60" width="29" height="58" rx="6"/><path d="m250 134 35 35m0-35-35 35"/></g>',
 independent:'<rect x="34" y="62" width="102" height="148" rx="13" fill="currentColor" fill-opacity=".09"/><path d="M53 93h61M53 120h61M53 147h40"/><g opacity=".3"><rect x="184" y="62" width="82" height="148" rx="13"/><path d="M200 95h48M200 122h48M200 149h34"/></g><circle cx="88" cy="206" r="25" fill="var(--panel)"/><path d="m76 206 8 9 17-18M150 106v62" stroke-dasharray="5 7"/><path d="m139 45 22 22m0-22-22 22"/><text x="48" y="43" fill="currentColor" stroke="none" font-size="13" font-weight="800" font-family="Arial,sans-serif">YOUR WORK</text>',
 hand:'<path d="M98 231v-45c0-17-9-32-18-46l-13-21c-7-14 10-24 20-13l22 25V53c0-19 25-19 25 0v57-78c0-19 25-19 25 0v78-65c0-19 25-19 25 0v68-47c0-19 25-19 25 0v92c0 22-6 32-15 47v26" fill="currentColor" fill-opacity=".06"/><path d="M125 189h51M232 80l13-8m-7 43h17M63 61l-12-9" opacity=".55"/>',
 integrity:'<path d="M150 31c30 21 54 27 90 31v65c0 56-35 91-90 116-55-25-90-60-90-116V62c36-4 60-10 90-31Z" fill="currentColor" fill-opacity=".07"/><path d="m108 131 28 29 57-61" stroke-width="10"/><path d="M104 192h92" opacity=".35"/>',
 extra:'<path d="M60 46h180c17 0 28 11 28 28v98c0 17-11 28-28 28h-94l-51 35v-35H60c-17 0-28-11-28-28V74c0-17 11-28 28-28Z" fill="currentColor" fill-opacity=".06"/><path d="M69 91h162M69 124h162M69 157h96" opacity=".65"/>',
};
function instructionArt(kind){
 const shape=artPaths[kind==='materials'?'desk':kind]||artPaths.extra;
 return '<svg class="instruction-art" viewBox="0 0 300 270" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'+shape+'</g></svg>';
}
function applySlidePalette(element,item,index){
 const p=slidePalettes[item.kind==='integrity'?5:index%slidePalettes.length];
 element.style.setProperty('--slide-color',p.color);element.style.setProperty('--slide-ink',p.ink);element.style.setProperty('--slide-rgb',p.rgb);
}
function emphasizeText(element,text){
 element.textContent='';
 const pieces=String(text).split(/(full name|student ID|EVERY page|empty seat|permitted materials only|approved materials|Work independently|Raise your hand|Stop writing immediately|recorded and reported)/gi);
 pieces.forEach((piece,index)=>{if(index%2){const strong=document.createElement('strong');strong.textContent=piece;element.append(strong)}else{element.append(document.createTextNode(piece))}});
}
function buildInstructionSlides(){
 c.instructions.forEach(item=>{if(item.text.trim())instructionSlides.push(item)});
 if(c.permittedMaterials)instructionSlides.push({title:'Permitted for this quiz',text:c.permittedMaterials,kind:'materials',label:'Materials',category:'YOUR APPROVED MATERIALS',tip:'Only bring the materials permitted for this assessment.'});
 c.extraComments.forEach((text,index)=>instructionSlides.push({title:c.extraComments.length===1?'One more thing…':'Additional instruction '+(index+1),text,kind:'extra',label:'Note '+(index+1),category:'PLEASE REMEMBER',tip:'If anything is unclear, ask the supervisor.'}));
 instructionSlides.push({title:'Protect the integrity of your work',text:c.integrityMessage,kind:'integrity',label:'Integrity',category:'ACADEMIC INTEGRITY',tip:'Follow staff directions. Suspected cheating is recorded and reported.'});
 instructionSlides.forEach((item,index)=>{
  const card=document.createElement('button');card.type='button';card.className='instruction-card'+(item.kind==='integrity'?' wide-card integrity-note':item.kind==='materials'?' materials-note':item.kind==='extra'?' extra-comments':'');
  card.setAttribute('aria-label','Present instruction '+(index+1)+': '+item.title);card.style.setProperty('--card-order',Math.min(index,8));applySlidePalette(card,item,index);
  const art=document.createElement('div');art.className='card-icon';art.setAttribute('aria-hidden','true');art.innerHTML=instructionArt(item.kind);
  const content=document.createElement('div'),category=document.createElement('div'),heading=document.createElement('h2'),copy=document.createElement('p');
  category.className='card-category';category.textContent=String(index+1).padStart(2,'0')+' / '+item.category;heading.textContent=item.title;copy.className='card-copy';emphasizeText(copy,item.text);
  content.append(category,heading,copy);card.append(art,content);card.onclick=()=>{setInstructionMode('presentation');showInstructionSlide(index)};
  $('instructionGrid').append(card);overviewCards.push(card);
  const step=document.createElement('button');step.type='button';step.className='step-link';step.setAttribute('aria-label','Instruction '+(index+1)+': '+item.title);step.title=item.title;
  const digit=document.createElement('span'),label=document.createElement('span');digit.className='step-digit';digit.textContent=String(index+1).padStart(2,'0');label.className='step-label';label.textContent=item.label;step.append(digit,label);step.onclick=()=>showInstructionSlide(index);
  $('slideSteps').append(step);stepButtons.push(step);
 });
}
function updateAutoplayControls(){
 $('autoToggle').textContent=autoplay?'Ⅱ Pause':'▶ Auto-play';$('autoToggle').classList.toggle('playing',autoplay);$('autoToggle').setAttribute('aria-pressed',String(autoplay));
 if(!autoplay)$('autoStatus').textContent=slideIndex===instructionSlides.length-1?'Final instruction · Show the timer when ready.':'Use ← → to navigate · P to play/pause';
}
function stopInstructionAutoplay(){
 autoplay=false;clearInterval(autoTimer);autoTimer=null;$('slideProgress').style.transform='scaleX(0)';updateAutoplayControls();
}
function resetSlideReadingTime(){
 const words=instructionSlides[slideIndex].text.trim().split(/\s+/).filter(Boolean).length;
 autoDuration=Math.max(c.instructionInterval*1000,2500+words*350);autoTarget=Date.now()+autoDuration;
}
function showInstructionSlide(index,manual=true){
 if(manual)stopInstructionAutoplay();
 slideIndex=Math.max(0,Math.min(instructionSlides.length-1,index));
 const item=instructionSlides[slideIndex],panel=$('instructionSpotlight');
 applySlidePalette(panel,item,slideIndex);$('slideArt').innerHTML=instructionArt(item.kind);
 $('slideCategory').textContent=String(slideIndex+1).padStart(2,'0')+' / '+item.category;$('slideTitle').textContent=item.title;emphasizeText($('slideBody'),item.text);$('slideTip').textContent=item.tip;
 $('slideCopy').scrollTop=0;panel.setAttribute('aria-label','Instruction '+(slideIndex+1)+' of '+instructionSlides.length+': '+item.title);
 $('slideCount').textContent=instructionMode==='overview'?instructionSlides.length+' instructions · select a card':'Instruction '+String(slideIndex+1).padStart(2,'0')+' of '+String(instructionSlides.length).padStart(2,'0');
 stepButtons.forEach((step,i)=>{step.classList.toggle('active',i===slideIndex);step.setAttribute('aria-current',i===slideIndex?'step':'false')});
 $('previousInstruction').disabled=slideIndex===0;$('nextInstruction').disabled=slideIndex===instructionSlides.length-1;
 panel.classList.remove('entering');void panel.offsetWidth;panel.classList.add('entering');
 const step=stepButtons[slideIndex];if(currentPage==='instructions'&&instructionMode==='presentation'&&typeof step.scrollIntoView==='function')step.scrollIntoView({block:'nearest',inline:'nearest',behavior:'auto'});
 if(autoplay)resetSlideReadingTime();updateAutoplayControls();
}
function setInstructionMode(mode){
 instructionMode=mode;const overview=mode==='overview';if(overview)stopInstructionAutoplay();
 $('instructionGrid').hidden=!overview;$('instructionSpotlight').hidden=overview;$('instructionNavigator').hidden=overview;
 $('presentMode').classList.toggle('active',!overview);$('overviewMode').classList.toggle('active',overview);$('presentMode').setAttribute('aria-pressed',String(!overview));$('overviewMode').setAttribute('aria-pressed',String(overview));
 showInstructionSlide(slideIndex,false);
}
function updateInstructionAutoplay(){
 if(!autoplay)return;if(currentPage!=='instructions'||instructionMode!=='presentation'||document.hidden){stopInstructionAutoplay();return}
 let remaining=Math.max(0,autoTarget-Date.now());
 if(remaining<=0){if(slideIndex===instructionSlides.length-1){stopInstructionAutoplay();return}showInstructionSlide(slideIndex+1,false);remaining=autoDuration}
 $('slideProgress').style.transform='scaleX('+Math.min(1,1-remaining/autoDuration)+')';$('autoStatus').textContent='Next instruction in '+Math.ceil(remaining/1000)+'s · P to pause';
}
function toggleInstructionAutoplay(){
 if(autoplay){stopInstructionAutoplay();return}
 if(currentPage!=='instructions')return;
 setInstructionMode('presentation');if(slideIndex===instructionSlides.length-1)showInstructionSlide(0,false);
 autoplay=true;resetSlideReadingTime();clearInterval(autoTimer);autoTimer=setInterval(updateInstructionAutoplay,100);updateAutoplayControls();updateInstructionAutoplay();
}
buildInstructionSlides();setInstructionMode(instructionMode);
function showPage(page){
 currentPage=page;const instructions=page==='instructions';
 if(!instructions)stopInstructionAutoplay();
 $('instructionsPage').hidden=!instructions;$('timerPage').hidden=instructions;
 $('instructionFooter').hidden=!instructions;$('timerFooter').hidden=instructions;
 $('instructionsTab').classList.toggle('active',instructions);$('timerTab').classList.toggle('active',!instructions);
 $('instructionsTab').setAttribute('aria-pressed',String(instructions));$('timerTab').setAttribute('aria-pressed',String(!instructions));
 $('shell').classList.toggle('instructions-mode',instructions);
 $('subtitle').textContent=instructions?'A few simple steps before we begin':c.subtitle;
 render();
}
function fmt(s){s=Math.max(0,Math.round(s));let h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return h?`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`:`${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`}
function tone(f=650,d=.16){if(!c.sound)return;try{let a=new(AudioContext||webkitAudioContext),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=f;g.gain.setValueAtTime(.13,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d);o.start();o.stop(a.currentTime+d)}catch(e){}}
function announce(text,seconds=3){if(currentPage!=='timer')showPage('timer');clearTimeout(bannerTimer);$('banner').textContent=text;$('banner').classList.add('show');tone();if(seconds<3600)bannerTimer=setTimeout(()=>$('banner').classList.remove('show'),seconds*1000)}
function render(){
 let p=total?Math.max(0,left/total*100):0,color=phase==='reading'?'#2f8cff':p<=c.red?'#ff4d5e':p<=c.amber?'#ffb020':'#2ed47a',thickness=p<=c.flash?34:p<=c.red?29:p<=c.amber?25:22;
 document.documentElement.style.setProperty('--accent',color);document.documentElement.style.setProperty('--glow',color+'66');document.documentElement.style.setProperty('--banner-border',color);
 $('ring').style.strokeDashoffset=L*(1-p/100);$('ring').style.strokeWidth=thickness;
 $('phase').textContent=ended?'FINISHED':phase==='reading'?'📖 READING TIME':'✍ WRITING TIME';$('clock').textContent=fmt(left);
 $('pct').innerHTML='<strong>'+Math.ceil(p)+'%</strong><br><span style="font-size:.72em;letter-spacing:2px">REMAINING</span>';
 $('elapsed').textContent='Elapsed '+fmt(elapsed);
 $('shell').classList.toggle('flash',currentPage==='timer'&&p<=c.flash&&running);
 $('start').textContent=running?'Running':'▶ '+(elapsed?'Resume':'Start');$('endScreen').classList.toggle('show',ended);
 const status=ended?'Time expired':running?`${phase==='reading'?'Reading':'Writing'} · ${fmt(left)} remaining`:elapsed?`Paused · ${fmt(left)} remaining`:'Timer ready';
 if($('pageStatus').textContent!==status)$('pageStatus').textContent=status;
}
function finishTime(){let d=new Date(Date.now()+left*1000+(phase==='reading'?c.exam*1000:0));$('headerFinish').textContent='Finish time: '+d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}
function tick(){if(!running)return;let previous=left;left=Math.max(0,(target-Date.now())/1000);elapsed=total-left;if(phase==='exam')c.milestones.forEach(m=>{if(previous>m*60&&left<=m*60&&!said.has(m)){said.add(m);announce(`${m} minute${m===1?'':'s'} remaining`)}});if(left<=0){if(phase==='reading'){phase='exam';total=c.exam;left=total;elapsed=0;target=Date.now()+left*1000;said.clear();announce('READING TIME ENDED — WRITING TIME STARTS NOW',4);finishTime()}else{running=false;ended=true;clearInterval(timer);announce(c.endMessage,86400);tone(420,.5)}}render()}
function collapseSidebar(){if(!c.collapseSidebar)return;try{const b=window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"] button');if(b)b.click()}catch(e){}}
function start(){if(!running&&!ended){running=true;target=Date.now()+left*1000;timer=setInterval(tick,200);finishTime();render();collapseSidebar()}}
function pause(){if(running){tick();running=false;clearInterval(timer);render()}}
function reset(){if(locked)return;const ok=window.confirm('Reset the timer and return to the initial reading/exam time?');if(!ok)return;running=false;ended=false;clearInterval(timer);clearTimeout(bannerTimer);phase=c.reading?'reading':'exam';total=c.reading||c.exam;left=total;elapsed=0;said.clear();$('banner').classList.remove('show');$('headerFinish').textContent='Finish time: --:--';render()}
function adjust(seconds){if(locked)return;left=Math.max(0,left+seconds);total=Math.max(total,left);if(running)target=Date.now()+left*1000;finishTime();render()}
function manualWarning(text,seconds=5){announce(text,seconds)}
function toggleLock(){locked=!locked;['plus','plus5','plus10','minus','reset'].forEach(id=>$(id).disabled=locked);$('lock').textContent=locked?'🔓 Unlock Controls':'🔒 Lock Controls';$('lock').classList.toggle('lock-active',locked)}
$('start').onclick=start;$('pause').onclick=pause;$('reset').onclick=reset;$('plus').onclick=()=>adjust(60);$('plus5').onclick=()=>adjust(300);$('plus10').onclick=()=>adjust(600);$('minus').onclick=()=>adjust(-60);$('warn15').onclick=()=>manualWarning('⚠ 15 MINUTES REMAINING',5);$('warn5').onclick=()=>manualWarning('⚠ 5 MINUTES REMAINING',5);$('stopmsg').onclick=()=>manualWarning('STOP WRITING NOW',8);$('lock').onclick=toggleLock;
async function toggleFullscreen(){try{if(document.fullscreenElement){await document.exitFullscreen()}else{await $('shell').requestFullscreen()}}catch(e){console.warn('Full screen is unavailable in this browser. Use the browser full-screen option instead.')}}
$('full').onclick=toggleFullscreen;$('instructionsFull').onclick=toggleFullscreen;
$('instructionsTab').onclick=()=>showPage('instructions');$('timerTab').onclick=()=>showPage('timer');$('showTimer').onclick=()=>showPage('timer');
$('presentMode').onclick=()=>setInstructionMode('presentation');$('overviewMode').onclick=()=>setInstructionMode('overview');$('autoToggle').onclick=toggleInstructionAutoplay;
$('previousInstruction').onclick=()=>showInstructionSlide(slideIndex-1);$('nextInstruction').onclick=()=>showInstructionSlide(slideIndex+1);
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopInstructionAutoplay()});
document.querySelectorAll('.controls').forEach(control=>control.classList.add('controls-visible'));
document.addEventListener('keydown',e=>{
 if(e.repeat||e.ctrlKey||e.metaKey||e.altKey||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
 const key=e.key.toLowerCase();
 if(key==='i')showPage('instructions');if(key==='t')showPage('timer');if(key==='f')toggleFullscreen();
 if(currentPage==='instructions'){
  if(e.key==='ArrowRight'){e.preventDefault();setInstructionMode('presentation');showInstructionSlide(slideIndex+1)}
  if(e.key==='ArrowLeft'){e.preventDefault();setInstructionMode('presentation');showInstructionSlide(slideIndex-1)}
  if(e.key==='Home'){e.preventDefault();setInstructionMode('presentation');showInstructionSlide(0)}
  if(e.key==='End'){e.preventDefault();setInstructionMode('presentation');showInstructionSlide(instructionSlides.length-1)}
  if(key==='p')toggleInstructionAutoplay();if(key==='o')setInstructionMode(instructionMode==='overview'?'presentation':'overview');
 }
 if(currentPage==='timer'){
  if(e.code==='Space'){e.preventDefault();running?pause():start()}
  if(key==='r')reset();if(key==='l')toggleLock();
 }
});
showPage(c.startPage);
if(c.instructionAutoplay&&currentPage==='instructions'&&instructionMode==='presentation')toggleInstructionAutoplay();
</script>
</body>
</html>""".replace("__CONFIG__", config_json)

st.caption("Projector preview • Present one instruction at a time, show the overview, or use Auto-play. Switching to the timer preserves the countdown.")
components.html(html, height=820, scrolling=False)
with st.expander("Keyboard controls"):
    st.write(
        "**I:** instructions  |  **T:** timer  |  **F:** full screen  |  "
        "**← / →:** previous/next instruction  |  **P:** play/pause instructions  |  "
        "**O:** presentation/overview  |  **Home / End:** first/last instruction  |  "
        "**Space:** start/pause on the timer page  |  "
        "**R:** reset on the timer page  |  **L:** lock/unlock on the timer page"
    )
with st.expander("JCU policy reference (staff)"):
    st.markdown(
        "**Checked 23 November 2026.** JCU requires staff to report suspected "
        "academic misconduct with supporting evidence (Student Academic "
        "Misconduct Procedure, clause 1.1). Findings and penalties are decided "
        "through the University's process, with an opportunity for the student "
        "to respond (clauses 4–6). The published procedures do not establish an "
        "automatic 'first warning, second incident: collect the paper and dismiss "
        "the student' rule. A warning does not replace reporting suspected "
        "misconduct.\n\n"
        "The directions about names, separating stapled pages and seating are "
        "classroom instructions. Use the permitted materials specified for the "
        "assessment and honour approved assessment adjustments.\n\n"
        f"[Student Academic Misconduct Procedure]({JCU_MISCONDUCT_URL}) · "
        f"[Examinations Procedure for Students]({JCU_EXAM_URL})"
    )
