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
LEARNJCU_URL = "https://learn.jcu.edu.au/"
JCU_SURVEY_GUIDE_URL = (
    "https://www.jcu.edu.au/__data/assets/pdf_file/0008/2306555/"
    "YourJCU-Subject-and-Teaching-Survey-Students.pdf"
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
OVERVIEW_INSTRUCTIONS = [
    ("Write your name", "Write your full name and student ID before answering any questions."),
    ("Name every loose page", "Separating pages? Write your full name and student ID on EVERY page first. Hand in all pages together."),
    ("Sit apart", "Spread out. Leave an empty seat between classmates where possible. Follow staff seating directions."),
    ("Clear your desk", "Permitted materials only. Put bags away. Switch off and put away phones, watches and unapproved devices."),
    ("Eyes on your paper", "Work independently. Do not look at others' answers or show yours. No talking or sharing materials."),
    ("Follow staff directions", "Raise your hand for help. Start only when instructed. Stop writing immediately when told. Hand in every page."),
]
INTEGRITY_MESSAGE = (
    "Looking at others' answers or other suspected cheating will be "
    "recorded and reported under JCU's Student Academic Misconduct Procedure. "
    "Follow any warning or direction immediately. A warning does not prevent "
    "reporting; penalties follow the University process."
)

def theme_palette(bg, panel, ring, accent, second, third, track,
                  text="#FAF7FF", muted="#D9CFEB", light=False):
    return {
        "bg": bg, "panel": panel, "ring-colour": ring, "track": track,
        "text": text, "clock-text": text, "muted": muted,
        "accent": accent, "brand": accent, "glow": accent + "30",
        "brand-soft": accent + "22", "brand-border": accent + "85",
        "ambient-a": accent + "50", "ambient-b": second + "40",
        "ambient-c": third + "45", "face-sheen": ring + "1C",
        "banner-bg": panel, "banner-text": text, "banner-border": ring,
        "button-text": muted, "button-hover": text,
        "reading": accent if light else second,
        "first-warning": "#A86000" if light else "#FFD477",
        "final-warning": "#C22D59" if light else "#FF8DA9", "light": light,
    }


# Complete, coordinated palettes. There are no legacy themes in this menu.
THEMES = {
    "Aurora": theme_palette("#101B37", "#1C3154", "#73FFE4", "#B497FF", "#FF7CCC", "#73CFFF", "#425779", muted="#C2DBE9"),
    "Candy Pop": theme_palette("#351638", "#4C2356", "#7AEBFF", "#FF79CA", "#C59AFF", "#FFD477", "#784B7D"),
    "Sunset Glow": theme_palette("#39152F", "#55243B", "#FFD27B", "#FF8B98", "#BC8EFF", "#FFBC67", "#84505F"),
    "Tropical Lagoon": theme_palette("#063538", "#0D4B50", "#6AF2DF", "#FF91A6", "#FFDF83", "#63C9FF", "#35737A", muted="#C1E5E4"),
    "Electric Violet": theme_palette("#24104B", "#3B1E69", "#DFBBFF", "#AAED77", "#FF93D2", "#77CCFF", "#694B91"),
    "Coral Reef": theme_palette("#34203E", "#4D304F", "#FFA3AD", "#71ECD8", "#FFD183", "#AEB5FF", "#785474"),
    "Peach Sorbet": theme_palette("#FFF0E5", "#FFF8F2", "#AB2960", "#A24AA0", "#FD9675", "#A991E9", "#E2BFD0", text="#512644", muted="#80526B", light=True),
    "Neon Arcade": theme_palette("#10172B", "#172442", "#D7FF72", "#FF69BD", "#6DE7FF", "#B995FF", "#344B70"),
    "Cosmic Burst": theme_palette("#151446", "#272662", "#FFB873", "#78E1FF", "#F498E2", "#B7A0FF", "#504D8B"),
    "Mango Fiesta": theme_palette("#38230F", "#50351B", "#FFE284", "#FF8BBD", "#6CE1CF", "#FFA059", "#7D6034", muted="#EAD7BD"),
    "Cherry Blossom": theme_palette("#FFF0F5", "#FFF9FC", "#C22D74", "#8E4BCA", "#FF85B1", "#83CAE6", "#EDCADA", text="#522B4B", muted="#885B76", light=True),
    "Blueberry Fizz": theme_palette("#112654", "#1B3E70", "#95DBFF", "#F49CDB", "#B4B1FF", "#7FF1C8", "#456A99", muted="#CEDCF4"),
    "Citrus Splash": theme_palette("#153426", "#244E38", "#D1FA7F", "#FFBC66", "#77E7ED", "#F9D669", "#48785D", muted="#D1E7CE"),
    "Flamingo Party": theme_palette("#401330", "#5B2347", "#FFA8C2", "#8DE9E1", "#FFD67F", "#B7A3FF", "#85506C"),
    "Lavender Dream": theme_palette("#F1EDFF", "#FFFBFF", "#7537B0", "#D33A85", "#B39AF1", "#FFAE9A", "#D7C9EF", text="#3C2A65", muted="#6C5B88", light=True),
    "Dragonfruit": theme_palette("#320F42", "#4A205C", "#DBFF81", "#FF76BC", "#80E6FF", "#FFC97B", "#784387"),
    "Bubblegum Sky": theme_palette("#E7F6FF", "#F7FCFF", "#6640BE", "#C33392", "#77CCE6", "#FFB7D6", "#C3D8EF", text="#263958", muted="#576B8B", light=True),
    "Festival Lights": theme_palette("#23123F", "#382052", "#FFDB83", "#FF7AD7", "#79EDE4", "#AD9DFF", "#62427F"),
}
COLOUR_FIELDS = {
    "look_ring": "ring-colour", "look_clock": "clock-text",
    "look_face": "panel", "look_track": "track", "look_background": "bg",
    "look_text": "text", "look_muted": "muted", "look_reading": "reading",
    "look_first_warning": "first-warning", "look_final_warning": "final-warning",
}


def load_theme_colours():
    selected = THEMES[st.session_state["display_theme_v3"]]
    for widget_key, palette_key in COLOUR_FIELDS.items():
        st.session_state[widget_key] = selected[palette_key]


if st.session_state.get("display_theme_v3") not in THEMES:
    st.session_state["display_theme_v3"] = "Aurora"
for widget_key, palette_key in COLOUR_FIELDS.items():
    # Keep optional pickers' values when their controls are hidden.
    st.session_state[widget_key] = st.session_state.get(
        widget_key, THEMES[st.session_state["display_theme_v3"]][palette_key]
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
[data-testid="stSidebar"] {background:linear-gradient(165deg,#161c3d,#0b1730 65%);border-right:1px solid #37416b;}
[data-testid="stSidebar"] [data-testid="stExpander"] {border:1px solid #394569;border-radius:14px;background:rgba(255,255,255,.025);margin-bottom:8px;}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {font-weight:750;padding-top:12px;padding-bottom:12px;}
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
    st.caption("Settings update immediately. Open a section to customise your display.")
    with st.expander("1 · Timer setup", expanded=True):
        title = st.text_input("Exam or subject title", "ME3512 Examination")
        subtitle = st.text_input("Subtitle", "Please manage your time carefully")
        c1, c2 = st.columns(2)
        with c1:
            hours = st.number_input("Exam hours", 0, 12, 1, 1)
        with c2:
            minutes = st.number_input("Exam minutes", 0, 59, 50, 1)
        reading_on = st.toggle("Include reading time", True)
        reading_minutes = st.number_input("Reading minutes", 0, 120, 10, 1, disabled=not reading_on)
        st.caption("Changing these durations prepares a fresh timer. Use the live + / − controls to change time during an exam.")
        collapse_sidebar = st.toggle("Collapse sidebar on start", True)

    with st.expander("2 · Colours & themes"):
        theme = st.selectbox(
            "Display theme", list(THEMES), key="display_theme_v3",
            on_change=load_theme_colours,
        )
        chosen = THEMES[theme]
        swatches = "".join(
            f'<span style="display:inline-block;width:32px;height:12px;'
            f'border-radius:5px;background:{chosen[name]};margin-right:5px"></span>'
            for name in ("ring-colour", "brand", "reading", "text", "panel")
        )
        st.markdown(f'<div style="margin:0 0 12px">{swatches}</div>', unsafe_allow_html=True)
        st.caption("18 vibrant palettes. Choosing a theme loads its coordinated colours. Fine-tune any colour below.")
        left_col, right_col = st.columns(2)
        with left_col:
            ring_colour = st.color_picker("Timer ring", key="look_ring")
            st.color_picker("Timer face", key="look_face")
            st.color_picker("Headings", key="look_text")
            st.color_picker("Background", key="look_background")
        with right_col:
            st.color_picker("Timer numbers", key="look_clock")
            st.color_picker("Ring track", key="look_track")
            st.color_picker("Supporting text", key="look_muted")
        separate_reading = st.toggle("Use a different reading ring colour", False, key="separate_reading_v3")
        reading_colour = (
            st.color_picker("Reading ring", key="look_reading")
            if separate_reading else ring_colour
        )
        st.caption("Timer ring applies to both reading and writing unless you enable a separate reading colour or warning colours.")
        st.button("Restore this theme's colours", on_click=load_theme_colours)
        show_logo = st.toggle("Show subtle JCU shield", True)

    with st.expander("3 · Warnings & sound"):
        change_ring_colour = st.toggle("Change ring colour for warnings", False, key="warning_colours_v3")
        amber, red = 50, 20
        amber_colour = st.session_state["look_first_warning"]
        red_colour = st.session_state["look_final_warning"]
        if change_ring_colour:
            amber = st.slider("First colour change below (%)", 10, 80, 50, 5)
            red = st.slider("Final colour change below (%)", 1, 40, 20, 1)
            first_col, final_col = st.columns(2)
            with first_col:
                amber_colour = st.color_picker("First warning ring", key="look_first_warning")
            with final_col:
                red_colour = st.color_picker("Final warning ring", key="look_final_warning")
            st.caption("Warning ring colours replace the writing ring colour at these thresholds.")
        pulse_style = st.selectbox("Final-minute pulse", ["Subtle", "Off", "Gentle"])
        pulse_minutes = st.number_input("Pulse in final minutes", 1, 15, 5, 1)
        st.caption("A slow pulse on the ring only. The page and timer text stay steady.")
        sound = st.toggle("Sound alerts", True)
        milestones_raw = st.text_input("Warnings at minutes remaining", "30, 15, 5, 1")
        end_message = st.text_input("End message", "TIME EXPIRED — STOP WRITING")

    with st.expander("4 · Before the quiz"):
        start_with_instructions = st.toggle("Open on instructions page", True)
        instruction_view = st.selectbox("Instruction display", ["Presentation", "All instructions"])
        instruction_autoplay = st.toggle("Auto-play instructions", False)
        instruction_interval = st.slider("Seconds per instruction", 8, 30, 14, 1)
        animate_instructions = st.toggle("Animate instructions", True)
        instruction_font_size = st.slider("Instruction text size", 18, 32, 22, 1)
        permitted_materials = st.text_area(
            "Permitted materials for this quiz",
            "Standard stationery. Calculators, notes and other materials only if "
            "expressly permitted for this quiz.", height=100, max_chars=600,
        )
        extra_comments_raw = st.text_area(
            "Extra comments (one per line)", "", height=100, max_chars=3000,
            help="These appear below the main instructions. Leave blank if not needed.",
        )
        st.caption("Edit the six main instructions below. Presentation builds the board one point at a time.")
        instruction_cards = []
        for index, (heading, default_text) in enumerate(DEFAULT_INSTRUCTIONS):
            text = st.text_area(
                heading, default_text, height=115,
                max_chars=1000, key=f"instruction_{index}",
            )
            instruction_cards.append({
                "title": heading, "text": text, **INSTRUCTION_VISUALS[index],
                "overviewTitle": OVERVIEW_INSTRUCTIONS[index][0],
                "overviewText": (
                    OVERVIEW_INSTRUCTIONS[index][1]
                    if text.strip() == default_text.strip() else text
                ),
            })

    with st.expander("5 · Subject survey"):
        survey_subject = st.text_input("Survey subject name (optional)", "")
        survey_message = st.text_area(
            "Survey reminder message",
            "Your feedback inspires new ideas, helps us fix issues, and shows us "
            "what is working well. Please share your experience so we can improve "
            "the subject.", height=100, max_chars=800,
        )
        survey_total = st.number_input("Students in subject (0 = not set)", 0, 10000, 0, 1)
        survey_completed = st.number_input("Completed survey responses", 0, 10000, 0, 1)
        st.caption("Enter current counts from the survey portal; these do not update automatically.")
    st.caption("Use + / − below the timer to change a live countdown. Adding time after it ends resumes it immediately.")

survey_participation_known = survey_total > 0 and survey_completed <= survey_total
if survey_total > 0 and survey_completed > survey_total:
    st.sidebar.warning("Completed responses cannot exceed the number of students.")
if red >= amber:
    red = amber - 1
    st.sidebar.info("The final colour change has been placed below the first warning threshold.")
# The selected theme supplies every colour; visible pickers override it directly.
display_palette = {**THEMES[theme]}
for widget_key, palette_key in COLOUR_FIELDS.items():
    display_palette[palette_key] = st.session_state[widget_key]
display_palette.update({
    "banner-bg": display_palette["panel"],
    "banner-text": display_palette["text"],
    "face-sheen": ring_colour + "1C",
})

try:
    milestones = sorted(
        {int(item.strip()) for item in milestones_raw.split(",") if item.strip() and int(item.strip()) > 0},
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
    "ringColour": ring_colour,
    "readingColour": reading_colour,
    "amberColour": amber_colour,
    "redColour": red_colour,
    "changeRingColour": change_ring_colour,
    "pulseStyle": pulse_style,
    "pulseMinutes": int(pulse_minutes),
    "sound": sound,
    "milestones": milestones,
    "endMessage": end_message,
    "theme": theme,
    "lightTheme": THEMES[theme]["light"],
    "palette": {
        key: value for key, value in display_palette.items()
        if isinstance(value, str) and key not in ("reading", "first-warning", "final-warning")
    },
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
    "surveySubject": survey_subject.strip(),
    "surveyMessage": survey_message.strip(),
    "surveyTotal": int(survey_total),
    "surveyCompleted": int(survey_completed),
    "surveyParticipationKnown": bool(survey_participation_known),
    "learnJcuUrl": LEARNJCU_URL,
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
body.bright-theme{--button-hover:var(--text)}
.shell{background:radial-gradient(ellipse at 7% 5%,var(--ambient-a),transparent 54%),radial-gradient(ellipse at 96% 92%,var(--ambient-b),transparent 52%),radial-gradient(ellipse at 88% 7%,var(--ambient-c),transparent 44%),var(--bg)!important}
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
body.bright-theme .slide-kicker,body.bright-theme .slide-copy strong,body.bright-theme .card-category,body.bright-theme .card-copy strong,body.bright-theme .card-icon,body.bright-theme .spotlight-art{color:var(--slide-ink)}
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
.timer>svg{position:absolute;inset:-9%;width:118%;height:118%;padding:9%;overflow:visible;transform:rotate(-90deg);filter:none}.track,.progress{fill:none;stroke-width:22}.track{stroke:var(--track)}.progress{stroke:var(--accent);stroke-linecap:round}
.content{position:absolute;inset:15%;z-index:2;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:12px;text-align:center}.phase{width:100%;font-size:clamp(15px,1.55vw,23px);font-weight:850;letter-spacing:.11em;line-height:1.25;color:var(--accent)}.clock{width:100%;font-size:clamp(56px,7.4vw,119px);font-weight:900;letter-spacing:-.035em;line-height:1.05;font-variant-numeric:tabular-nums;text-shadow:0 5px 18px #0003;white-space:nowrap}.pct{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:clamp(16px,1.4vw,22px);line-height:1.2;color:var(--muted);font-weight:700}.pct-label{font-size:.64em;letter-spacing:.12em}
.banner{position:absolute;z-index:4;width:min(92%,900px);padding:30px 38px;border:3px solid var(--banner-border);border-radius:24px;background:var(--banner-bg);color:var(--banner-text);text-align:center;font-size:clamp(28px,4vw,57px);font-weight:950;line-height:1.15;letter-spacing:.3px;box-shadow:0 25px 80px #000b,0 0 35px var(--glow);opacity:0;transform:scale(.85);pointer-events:none;transition:.25s}.banner.show{opacity:1;transform:scale(1)}.markers{position:absolute;inset:0;z-index:1;pointer-events:none}.marker{position:absolute;width:9px;height:9px;border-radius:50%;background:var(--muted);box-shadow:0 0 0 3px var(--panel);opacity:.7}.m75{left:50%;top:3%;transform:translateX(-50%)}.m50{right:3%;top:50%;transform:translateY(-50%)}.m25{left:50%;bottom:3%;transform:translateX(-50%)}.m10{left:9%;top:69%}.end-screen{position:absolute;inset:0;z-index:8;display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;background:radial-gradient(circle,#75131d,#260207 72%);color:#fff;opacity:0;pointer-events:none;transition:.35s}.end-screen.show{opacity:1;pointer-events:auto}.end-main{font-size:clamp(58px,8vw,132px);font-weight:950;letter-spacing:2px}.end-sub{font-size:clamp(30px,4vw,68px);font-weight:900;margin-top:12px}.end-line{width:min(72%,900px);height:5px;background:#fff;margin:24px 0;border-radius:4px}
footer{text-align:center;position:relative;z-index:10;padding:4px 0 8px;overflow:visible}.meta{color:var(--muted);margin:0 0 10px}.controls{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:9px;opacity:1!important;visibility:visible!important;pointer-events:auto!important;transform:none!important;filter:none!important;position:relative;z-index:12}.controls:hover,.controls:focus-within,.controls.controls-visible{opacity:1!important;visibility:visible!important}.controls button{padding:11px 17px;border-radius:12px;border:1px solid var(--button-border);background:var(--button-bg);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);color:var(--button-text);font-size:15px;font-weight:750;cursor:pointer;box-shadow:none;opacity:1!important;visibility:visible!important;transition:color .22s ease,background .22s ease,border-color .22s ease,transform .22s ease}.controls button:hover,.controls button:focus-visible{color:var(--button-hover);background:rgba(84,112,148,.22);border-color:rgba(151,176,207,.46);transform:translateY(-1px);outline:none}.controls .primary{background:rgba(46,212,122,.10);color:#93bfa5;border-color:rgba(82,177,121,.25)}.controls .primary:hover{background:rgba(46,212,122,.18);color:#c8ead5;border-color:rgba(82,177,121,.45)}.controls button:disabled{opacity:.35;cursor:not-allowed;filter:grayscale(.45);box-shadow:none}.controls .lock-active{background:rgba(255,176,32,.14);color:#c9a761;border-color:rgba(255,196,91,.32)}
.shell:fullscreen{padding:clamp(18px,2vw,42px)}.shell:fullscreen .stage{padding:20px 34px}.shell:fullscreen .timer{width:min(60vh,68vw);height:min(60vh,68vw);max-width:760px;max-height:760px;margin:12px}.shell:fullscreen .clock{font-size:clamp(100px,12vw,210px)}.shell:fullscreen .phase{font-size:clamp(24px,2.5vw,40px)}.shell:fullscreen .pct{font-size:clamp(20px,2vw,32px)}.shell:fullscreen .title{font-size:clamp(38px,4vw,72px)}.shell:fullscreen .subtitle{font-size:clamp(18px,1.8vw,30px)}.shell:fullscreen .logo{height:clamp(65px,8vh,105px);max-width:140px;opacity:.25}.shell:fullscreen .banner{font-size:clamp(42px,5vw,82px);padding:42px}
@media(max-width:650px){.shell{padding:10px}.stage{padding:12px}.timer{min-width:280px;min-height:280px;width:min(50vh,82vw);height:min(50vh,82vw);margin:8px}.logo{height:42px}.clock{letter-spacing:-2px}.banner{padding:22px 18px}}
/* The overview is a full-height instruction board; presentation keeps its hero. */
.instruction-grid{--overview-font:30px;--overview-columns:3;--overview-rows:3;display:grid;grid-template-columns:repeat(var(--overview-columns),minmax(0,1fr));grid-template-rows:repeat(var(--overview-rows),minmax(0,1fr));grid-auto-flow:row;gap:clamp(10px,1vw,16px);align-content:stretch;align-items:stretch;padding:4px;overflow-x:hidden;overflow-y:auto;scrollbar-gutter:stable}
.instruction-card{position:relative;display:flex;flex-direction:column;gap:clamp(10px,1.1vh,16px);min-width:0;min-height:0;padding:clamp(14px,1.1vw,24px);border-radius:22px;overflow:hidden;box-shadow:0 8px 25px #0002;animation:none}
.instruction-card.wide-card{grid-column:span 1}
.card-heading{display:grid;grid-template-columns:50px minmax(0,1fr);align-items:center;gap:13px;flex-shrink:0;min-width:0}
.card-heading .card-icon{width:50px;height:50px;padding:5px;border-radius:14px;flex-shrink:0}
.card-heading .card-category{font-size:11px;line-height:1.2;letter-spacing:1.5px;margin-bottom:5px;font-weight:850}
.instruction-card .card-title{font-size:clamp(23px,calc(var(--overview-font,30px) * 1.13),39px);font-weight:850;line-height:1.13;letter-spacing:-.55px;margin:0;text-wrap:balance}
.instruction-card .card-copy{font-size:var(--overview-font,30px);line-height:1.32;letter-spacing:-.12px;flex-shrink:0;margin:0;text-wrap:pretty}
.instruction-card::after{content:'';position:absolute;left:0;top:18px;bottom:18px;width:3px;border-radius:0 4px 4px 0;background:var(--slide-color);opacity:.7}
.instruction-grid.overview-scroll{grid-template-rows:repeat(var(--overview-rows),minmax(max-content,1fr));align-content:stretch}
.instruction-grid.overview-scroll .instruction-card{min-height:150px;overflow:visible}
.shell.overview-mode,.shell.overview-mode:fullscreen{padding:clamp(12px,1.25vw,24px)}
.shell.overview-mode .title{font-size:clamp(27px,2.5vw,46px);line-height:1.12}
.shell.overview-mode .subtitle{display:none}
.shell.overview-mode .logo{height:44px;max-width:70px}
.shell.overview-mode .page-nav{margin:8px 0 5px;gap:8px}
.shell.overview-mode .page-nav button{padding:7px 15px;font-size:14px}
.shell.overview-mode .instructions-page{padding:4px 0 2px;gap:9px}
.shell.overview-mode .briefing-tool{padding:7px 12px}
.shell.overview-mode footer{padding:0 0 2px}
.shell.overview-mode .instruction-note{margin:5px 0 7px;font-size:13px}
.shell.overview-mode .controls button{padding:9px 15px}
.build-caption{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-shrink:0;font-size:11px;line-height:1.2;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);padding:0 4px}
.build-caption span:last-child{letter-spacing:.3px;text-transform:none;font-weight:650}
.instructions-page.building .spotlight{padding:18px 26px;grid-template-columns:minmax(105px,.48fr) minmax(0,2fr);gap:24px}
.instructions-page.building .spotlight-art{max-width:175px;border-radius:20px}
.instructions-page.building .slide-kicker{font-size:12px;margin-bottom:6px}
.instructions-page.building .slide-title{font-size:clamp(28px,2.65vw,46px);margin-bottom:10px}
.instructions-page.building .slide-copy{font-size:clamp(21px,1.7vw,30px);line-height:1.4}
.instructions-page.building .slide-tip{display:none}
.instruction-grid.build-grid{flex:0 0 var(--build-height,160px);max-height:46%;gap:9px;padding:2px 4px 4px;scrollbar-gutter:auto}
.build-grid .instruction-card{padding:10px 13px;gap:7px;border-radius:15px;animation:cardSettle .35s ease both}
.build-grid .card-heading{grid-template-columns:30px minmax(0,1fr);gap:9px}
.build-grid .card-heading .card-icon{width:30px;height:30px;padding:3px;border-radius:9px}
.build-grid .card-heading .card-category{font-size:9px;letter-spacing:1.2px;margin-bottom:3px}
.build-grid .instruction-card .card-title{font-size:calc(var(--overview-font,20px) * 1.07);line-height:1.1;letter-spacing:-.25px}
.build-grid .instruction-card .card-copy{font-size:var(--overview-font,20px);line-height:1.28}
.build-grid .instruction-card::after{top:12px;bottom:12px;width:2px}
@keyframes cardSettle{from{opacity:.25;transform:translateY(-9px) scale(.98)}to{opacity:1;transform:translateY(0) scale(1)}}
@media(max-width:1050px){.instruction-grid{--overview-columns:2}.card-heading{grid-template-columns:40px minmax(0,1fr);gap:10px}.card-heading .card-icon{width:40px;height:40px}.instruction-card{padding:13px 16px}.instruction-card .card-title{letter-spacing:-.3px}}
@media(max-width:680px){.instruction-grid{--overview-columns:1}.shell.overview-mode .title{font-size:26px}.card-heading{grid-template-columns:38px minmax(0,1fr)}.card-heading .card-icon{width:38px;height:38px}.instructions-page.building .spotlight{grid-template-columns:minmax(0,1fr);padding:18px}.instructions-page.building .slide-title{font-size:28px}.instructions-page.building .slide-copy{font-size:21px}.build-caption{font-size:10px;letter-spacing:.8px}.build-caption span:last-child{display:none}}
.survey-mode{--accent:#c1a3ff;--glow:#ac85ff24}.survey-mode .header-finish{display:none}
.survey-page{--participation-color:#ffb865;display:flex;flex-direction:column;gap:18px;min-height:0;overflow-y:auto;padding:12px 8px 18px;scrollbar-color:var(--track) var(--bg)}
.survey-layout{display:grid;grid-template-columns:minmax(270px,.8fr) minmax(0,1.45fr);gap:clamp(20px,2.5vw,44px);align-items:stretch;flex:1;min-height:min-content}
.participation-card{position:relative;border:1px solid var(--track);border-radius:28px;background:radial-gradient(circle at 50% 26%,#ffb86514,transparent 60%),var(--panel);padding:clamp(20px,2.4vw,42px);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden}
.survey-eyebrow{margin:0 0 12px;font-size:14px;font-weight:850;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}
.survey-gauge{width:100%;max-width:370px;display:block;position:static;inset:auto;transform:none;padding:0;filter:none;overflow:visible}
.survey-gauge .gauge-track,.survey-gauge .gauge-progress{fill:none;stroke-width:20;stroke-linecap:round}.gauge-track{stroke:var(--track)}.gauge-progress{stroke:var(--participation-color);transition:stroke-dashoffset 1s ease,stroke .5s}
.gauge-needle{transform-origin:180px 180px;transition:transform 1s cubic-bezier(.2,.8,.2,1)}.gauge-needle line{stroke:var(--text);stroke-width:5;stroke-linecap:round}.gauge-needle circle{fill:var(--text)}
.gauge-tick{fill:var(--muted);font-size:13px;font-weight:750;font-family:inherit}.participation-value{font-size:clamp(50px,5.8vw,88px);font-weight:950;line-height:1;letter-spacing:-3px;margin:-5px 0 10px;color:var(--text);font-variant-numeric:tabular-nums}
.participation-count{color:var(--muted);font-size:clamp(17px,1.4vw,23px);line-height:1.4;max-width:360px}
.participation-status{font-size:clamp(21px,1.8vw,30px);font-weight:850;line-height:1.2;margin:22px 0 0;max-width:360px}
.survey-copy{display:flex;flex-direction:column;justify-content:center;min-width:0;padding:8px 0}
.survey-title{font-size:clamp(34px,3.7vw,65px);font-weight:900;letter-spacing:-1.4px;line-height:1.08;margin:0 0 16px;text-wrap:balance}
.survey-subject{font-size:18px;font-weight:800;line-height:1.3;color:var(--accent);margin:0 0 12px;overflow-wrap:anywhere}
.survey-message{font-size:clamp(21px,1.65vw,29px);line-height:1.45;color:var(--text);margin:0 0 20px;white-space:pre-line;overflow-wrap:anywhere}
.survey-route{list-style:none;display:grid;gap:10px;margin:0;padding:0;counter-reset:survey-step}
.survey-route li{counter-increment:survey-step;display:grid;grid-template-columns:34px minmax(0,1fr);align-items:start;gap:12px;padding:13px 15px;background:var(--panel);border:1px solid var(--track);border-radius:15px;font-size:clamp(18px,1.45vw,25px);line-height:1.35}
.survey-route li::before{content:counter(survey-step);display:grid;place-items:center;width:32px;height:32px;background:#ac85ff18;border:1px solid var(--track);border-radius:10px;color:var(--accent);font-size:16px;font-weight:900}
.survey-route strong{font-weight:850;color:var(--accent)}
.survey-thanks{font-size:16px;line-height:1.35;color:var(--muted);margin:17px 0 0}
.survey-open{display:inline-flex;align-items:center;justify-content:center;padding:11px 18px;border-radius:12px;border:1px solid var(--accent);background:var(--panel);color:var(--text);font-size:16px;font-weight:800;text-decoration:none;cursor:pointer}
.survey-open:hover,.survey-open:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.no-instruction-motion .survey-page *{transition:none!important}
@media(prefers-reduced-motion:reduce){.survey-page *{transition:none!important}}
@media(max-width:850px){.survey-layout{grid-template-columns:minmax(0,1fr)}.participation-card{padding:20px;display:grid;grid-template-columns:minmax(130px,.75fr) minmax(0,1fr);column-gap:15px}.participation-card .survey-eyebrow{grid-column:1/-1}.survey-gauge{grid-column:1;grid-row:2/5;max-width:250px}.participation-value{font-size:52px;margin:0 0 6px;grid-column:2}.participation-count{grid-column:2;font-size:16px}.participation-status{grid-column:2;font-size:20px;margin:10px 0 0}.survey-title{font-size:34px}.survey-copy{padding:0}.survey-message{font-size:21px}.survey-route li{font-size:19px}}
/* Timer text is centred in a flat disc; only the ring can pulse. */
.timer,.shell:fullscreen .timer{container-type:inline-size;width:var(--timer-size,48vh);height:var(--timer-size,48vh);min-width:0;min-height:0;max-width:760px;max-height:760px;perspective:none}
.clock,.shell:fullscreen .clock{font-size:clamp(24px,25cqw,190px);color:var(--clock-text,var(--text))}.clock.has-hours,.shell:fullscreen .clock.has-hours{font-size:clamp(24px,17cqw,130px)}
.phase,.shell:fullscreen .phase{font-size:clamp(12px,4.5cqw,30px);letter-spacing:.10em}.pct,.shell:fullscreen .pct{font-size:clamp(13px,4.6cqw,30px)}
.disc{transform:none;border:1px solid var(--brand-border);background:radial-gradient(ellipse at 30% 12%,var(--face-sheen),transparent 65%),linear-gradient(145deg,#ffffff0b,transparent 70%),var(--panel);box-shadow:0 20px 60px #0004,inset 0 1px 0 #ffffff12}
.progress{stroke:var(--ring-colour);animation:none;stroke-width:22!important;filter:drop-shadow(0 0 5px var(--ring-glow));transition:stroke .4s,stroke-dashoffset .2s linear}
.phase{color:var(--ring-colour)}
.title::after{content:'';display:block;width:110px;height:4px;border-radius:99px;margin:10px auto 0;background:linear-gradient(90deg,var(--brand),var(--ring-colour),var(--brand));opacity:.9}
.page-nav button.active{background:linear-gradient(135deg,var(--brand-soft),transparent),var(--panel);border-color:var(--brand);box-shadow:0 0 0 1px var(--brand-border)}
.instructions-mode,.survey-mode{--accent:var(--brand);--glow:var(--brand-soft)}
.progress.urgent{animation:quietRingPulse 6s ease-in-out infinite}
@keyframes quietRingPulse{0%,100%{filter:drop-shadow(0 0 4px var(--ring-glow)) brightness(1)}50%{filter:drop-shadow(0 0 6px var(--ring-glow)) brightness(var(--pulse-peak,1.035))}}
.controls{gap:8px}.control-group{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:6px}
.timer-actions{margin-bottom:9px}.timer-actions>.control-group+.control-group{padding-left:12px;border-left:1px solid var(--track)}
.controls button{color:var(--muted);background:var(--panel);border-color:var(--track);padding:10px 13px;font-size:14px}
.controls button:hover,.controls button:focus-visible{color:var(--text);border-color:var(--brand);background:var(--brand-soft)}
.controls .primary,.controls .primary:hover{background:var(--brand-soft);color:var(--text);border-color:var(--brand-border)}
.controls button:disabled{opacity:.4!important;transform:none;cursor:not-allowed}
.controls .lock-active{color:#dfaf55;border-color:#dfaf5566}
.timer-options button{font-size:12px;padding:8px 10px}.timer-options{gap:14px}
.custom-adjust{border:1px solid var(--track);border-radius:12px;padding:4px 6px}.custom-adjust label{font-size:12px;font-weight:700;color:var(--muted);padding-left:4px}
.custom-adjust input{width:55px;min-height:30px;border:1px solid var(--track);border-radius:7px;background:var(--bg);color:var(--text);font:inherit;font-size:14px;font-weight:750;text-align:center}
.custom-adjust input:focus-visible{outline:2px solid var(--brand);outline-offset:2px}.custom-adjust input:disabled{opacity:.45}
.meta{font-size:12px;margin-bottom:8px;min-height:17px}.meta #timeFeedback:not(:empty)::before{content:' · ';padding:0 4px}#timeFeedback{color:var(--text)}
.end-screen{border-radius:24px;padding:25px;overflow-y:auto;justify-content:safe center}.end-main{font-size:clamp(36px,6vw,88px)}.end-sub{font-size:clamp(22px,3.2vw,48px)}.end-line{margin:17px 0}
.end-extra{font:inherit;font-size:clamp(16px,1.5vw,24px);font-weight:850;padding:13px 24px;border:1px solid #fff8;border-radius:14px;background:#fff;color:#631927;cursor:pointer;box-shadow:0 6px 20px #0003}
.end-extra:disabled{opacity:.45;cursor:not-allowed}.end-extra:focus-visible{outline:3px solid #fff;outline-offset:5px}.end-help{max-width:520px;font-size:14px;line-height:1.5;color:#ffe2e7;margin:14px 0 0}
.end-screen:not(.show){visibility:hidden}
@media(prefers-reduced-motion:reduce){.progress,.progress.urgent{animation:none!important;transition:none!important}}
@media(max-width:650px){.content{inset:12%;gap:9px}.phase{font-size:14px}.clock{font-size:clamp(46px,10vw,76px)}.pct{font-size:16px}.timer-actions>.control-group+.control-group{border:0;padding-left:0}.controls button{padding:8px 10px;font-size:12px}.timer-options{gap:7px}.timer-options button{font-size:11px}.meta{font-size:11px}.end-help{font-size:12px}}
</style>
</head>
<body>
<div class="shell" id="shell">
<header><img class="logo" id="logo"><div class="title" id="title"></div><div class="subtitle" id="subtitle"></div><div class="header-finish" id="headerFinish">Finish time: --:--</div></header>
<nav class="page-nav" aria-label="Display pages"><button type="button" id="instructionsTab" aria-controls="instructionsPage" aria-pressed="false">Before the quiz</button><button type="button" id="timerTab" aria-controls="timerPage" aria-pressed="false">Timer</button><button type="button" id="surveyTab" aria-controls="surveyPage" aria-pressed="false">Subject survey</button><span class="page-status" id="pageStatus" role="timer" aria-live="off"></span></nav>
<main class="instructions-page" id="instructionsPage" aria-label="Before the quiz" tabindex="0" hidden>
<div class="briefing-toolbar">
<div class="briefing-label" id="slideCount" aria-live="polite" aria-atomic="true"></div>
<div class="briefing-tools" aria-label="Instruction presentation controls"><button class="briefing-tool" id="presentMode" aria-pressed="true">Presentation</button><button class="briefing-tool" id="overviewMode" aria-pressed="false">All instructions</button><button class="briefing-tool" id="autoToggle" aria-pressed="false">▶ Auto-play</button><button class="briefing-tool" id="replayBriefing" hidden>↺ Replay</button></div>
</div>
<section class="spotlight" id="instructionSpotlight" aria-roledescription="slide" aria-label="Quiz instruction">
<div class="spotlight-art" id="slideArt" aria-hidden="true"></div>
<div class="spotlight-copy" id="slideCopy"><p class="slide-kicker" id="slideCategory"></p><h2 class="slide-title" id="slideTitle"></h2><p class="slide-copy" id="slideBody"></p><p class="slide-tip" id="slideTip"></p></div>
<div class="slide-progress" aria-hidden="true"><span class="slide-progress-fill" id="slideProgress"></span></div>
</section>
<div class="build-caption" id="buildCaption" hidden><span id="buildCaptionText">Already covered</span><span>Each point stays here as we continue</span></div>
<div class="instruction-grid" id="instructionGrid" aria-label="All quiz instructions" hidden></div>
<div class="instruction-navigator" id="instructionNavigator"><button class="nav-arrow" id="previousInstruction" aria-label="Previous instruction">←</button><div class="step-area"><div class="step-track" id="slideSteps" aria-label="Go to an instruction"></div><div class="auto-status" id="autoStatus" aria-live="off"></div></div><button class="nav-arrow" id="nextInstruction" aria-label="Next instruction">→</button></div>
</main>
<main class="survey-page" id="surveyPage" aria-label="Subject survey reminder" hidden>
<div class="survey-layout">
<section class="participation-card" aria-label="Survey participation">
<h2 class="survey-eyebrow">Subject survey participation</h2>
<svg class="survey-gauge" viewBox="0 0 360 235" role="img" aria-labelledby="surveyGaugeTitle"><title id="surveyGaugeTitle">Survey participation</title><path class="gauge-track" d="M56 180 A124 124 0 0 1 304 180"/><path class="gauge-progress" id="surveyGaugeProgress" d="M56 180 A124 124 0 0 1 304 180" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/><g class="gauge-needle" id="surveyNeedle"><line x1="180" y1="180" x2="180" y2="79"/><circle cx="180" cy="180" r="9"/></g><text class="gauge-tick" x="41" y="218">0%</text><text class="gauge-tick" x="166" y="35">50%</text><text class="gauge-tick" x="286" y="218">100%</text></svg>
<div class="participation-value" id="surveyPercent">—</div><div class="participation-count" id="surveyCount"></div><p class="participation-status" id="surveyStatus"></p>
</section>
<section class="survey-copy">
<p class="survey-subject" id="surveySubject" hidden></p><h1 class="survey-title">Your feedback can make this subject better.</h1><p class="survey-message" id="surveyMessage"></p>
<ol class="survey-route"><li><span>Open <strong>LearnJCU</strong> and select <strong>Tools</strong>.</span></li><li><span>Choose <strong>YourJCU Survey Portal</strong>.</span></li><li><span>Select your subject’s survey, share your feedback and <strong>submit</strong>.</span></li></ol>
<p class="survey-thanks">Tell us what helped you learn and what could be improved. Thank you for sharing your experience.</p>
</section>
</div>
</main>
<main class="stage" id="timerPage" aria-label="Countdown timer" hidden>
<div class="timer"><div class="disc"></div><div class="markers"><span class="marker m75" title="75%"></span><span class="marker m50" title="50%"></span><span class="marker m25" title="25%"></span><span class="marker m10" title="10%"></span></div><svg viewBox="0 0 420 420"><circle class="track" cx="210" cy="210" r="180"/><circle class="progress" id="ring" cx="210" cy="210" r="180"/></svg><div class="content"><div class="phase" id="phase">READY</div><div class="clock" id="clock"></div><div class="pct" id="pct"></div></div></div>
<div class="banner" id="banner"></div><div class="end-screen" id="endScreen" aria-hidden="true"><div class="end-line"></div><div class="end-main">TIME EXPIRED</div><div class="end-sub" id="endSub">STOP WRITING NOW</div><div class="end-line"></div><button class="end-extra" id="endPlus5">+ 5 extra minutes</button><p class="end-help">Adding time resumes the countdown. More time controls are below.</p></div>
</main>
<footer>
<div id="instructionFooter"><div class="instruction-note">Approved assessment adjustments still apply. Do not begin until instructed.</div><div class="controls"><button class="primary" id="showTimer">▶ Show timer</button><button id="instructionsFull">⛶ Full Screen</button></div></div>
<div id="timerFooter" hidden>
<div class="meta"><span id="elapsed"></span><span id="timeFeedback" role="status" aria-live="polite"></span></div>
<div class="controls timer-actions"><div class="control-group"><button class="primary" id="start">▶ Start</button><button id="pause">Ⅱ Pause</button></div><div class="control-group" aria-label="Quick time adjustments"><button id="minus5" title="Subtract five minutes">− 5 min</button><button id="minus" title="Subtract one minute">− 1 min</button><button id="plus" title="Add one minute">+ 1 min</button><button id="plus5" title="Add five minutes, including after time expires">+ 5 min</button><button id="plus10" title="Add ten minutes">+ 10 min</button></div><button id="full">⛶ Full screen</button></div>
<div class="controls timer-options"><div class="control-group custom-adjust"><label for="adjustMinutes">Minutes</label><input id="adjustMinutes" type="number" min="1" max="720" step="1" value="5" inputmode="numeric"><button id="customMinus" title="Subtract the entered minutes">− Subtract</button><button id="customPlus" title="Add the entered minutes">+ Add</button></div><div class="control-group"><button id="warn15">⚠ 15 min</button><button id="warn5">⚠ 5 min</button><button id="stopmsg">■ Stop writing</button></div><div class="control-group"><button id="reset">↺ Reset</button><button id="lock">🔒 Lock</button></div></div>
</div>
<div id="surveyFooter" hidden><div class="controls"><a class="survey-open" id="learnJcuLink" target="_blank" rel="noopener noreferrer">Open LearnJCU ↗</a><button id="surveyFull">⛶ Full Screen</button><button id="surveyTimer">Return to timer</button></div></div>
</footer>
</div>
<script>
const c=__CONFIG__,$=id=>document.getElementById(id);
document.body.classList.toggle('bright-theme',c.lightTheme);
document.body.dataset.theme=c.theme;
// Apply on the body itself so no theme rule can hide a selected colour.
Object.entries(c.palette).forEach(([name,value])=>document.body.style.setProperty('--'+name,value));
document.body.style.setProperty('--pulse-peak',c.pulseStyle==='Gentle'?'1.075':'1.035');
$('title').textContent=c.title;$('subtitle').textContent=c.subtitle;
$('endSub').textContent=c.endMessage.replace(/^TIME EXPIRED\s*[—–:\-]?\s*/i,'')||'STOP WRITING NOW';
if(c.showLogo){$('logo').src=c.logo}else{$('logo').style.display='none'}
const L=2*Math.PI*180;$('ring').style.strokeDasharray=L;
let phase=c.reading?'reading':'exam',total=c.reading||c.exam,left=total,elapsed=0,running=false,ended=false,target=0,timer=null,said=new Set(),bannerTimer=null,locked=false;
let hasStarted=false,plannedExam=c.exam,endedAt=0,lastSavedAt=0,feedbackTimer=null;
let storagePath=location.pathname;
try{storagePath=window.parent.location.pathname}catch(e){}
const storageKey='examtimer-pro:live:v3:'+storagePath;
let currentPage=c.startPage;
document.documentElement.style.setProperty('--instruction-font',c.instructionFontSize+'px');
const prefersReducedMotion=typeof window.matchMedia==='function'&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!c.animateInstructions||prefersReducedMotion)$('shell').classList.add('no-instruction-motion');
function updateSurveyReminder(animate=false){
 $('surveySubject').textContent=c.surveySubject;$('surveySubject').hidden=!c.surveySubject;
 $('surveyMessage').textContent=c.surveyMessage;$('learnJcuLink').href=c.learnJcuUrl;
 const known=c.surveyParticipationKnown,percent=known?c.surveyCompleted/c.surveyTotal*100:0;
 const color=percent<30?'#ffb865':percent<70?'#f5d166':'#79e6bb';
 $('surveyPage').style.setProperty('--participation-color',color);
 $('surveyPercent').textContent=known?Math.round(percent)+'%':'—';
 $('surveyCount').textContent=known?c.surveyCompleted+' of '+c.surveyTotal+' students have responded.':'Add your voice to the feedback.';
 $('surveyStatus').textContent=!known?'Every response matters.':percent<30?'We need more voices.':percent<70?'Help us hear from more students.':'Thank you. Every voice still matters.';
 $('surveyGaugeTitle').textContent=known?'Survey participation: '+c.surveyCompleted+' of '+c.surveyTotal+' students.':'Survey participation figures have not been entered.';
 $('surveyNeedle').setAttribute('visibility',known?'visible':'hidden');
 const applyGauge=()=>{$('surveyGaugeProgress').style.strokeDashoffset=String(100-percent);$('surveyNeedle').style.transform='rotate('+(percent*1.8-90)+'deg)'};
 if(animate&&known&&c.animateInstructions&&!prefersReducedMotion&&typeof window.requestAnimationFrame==='function'){
  $('surveyGaugeProgress').style.strokeDashoffset='100';$('surveyNeedle').style.transform='rotate(-90deg)';
  window.requestAnimationFrame(()=>window.requestAnimationFrame(applyGauge));
 }else{applyGauge()}
}
updateSurveyReminder();
let instructionMode=c.instructionMode,slideIndex=0,autoplay=false,autoTimer=null,autoTarget=0,autoDuration=0;
let briefingComplete=false,overviewLayoutFrame=null;
const revealedInstructions=new Set();
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
function fitInstructionBoard(){
 const grid=$('instructionGrid');
 if(grid.hidden||currentPage!=='instructions'||!(grid.clientWidth>0)||!(grid.clientHeight>0))return;
 const visible=overviewCards.filter(card=>!card.hidden);if(!visible.length)return;
 const building=grid.classList.contains('build-grid'),width=grid.clientWidth;
 const availableColumns=building?(width>=1350?4:width>=850?3:width>=560?2:1):(width>=1050?3:width>=680?2:1);
 const columns=Math.min(availableColumns,visible.length);
 const rows=Math.ceil(visible.length/columns),lastSpan=columns-((visible.length-1)%columns);
 grid.style.setProperty('--overview-columns',columns);grid.style.setProperty('--overview-rows',rows);
 overviewCards.forEach(card=>card.style.gridColumn='span 1');visible[visible.length-1].style.gridColumn='span '+lastSpan;
 if(building)grid.style.setProperty('--build-height',Math.min(350,Math.max(116,rows*134))+'px');
 grid.classList.remove('overview-scroll');
 const minimum=building?16:20,goal=building?20:Math.min(38,Math.max(30,c.instructionFontSize+8));
 const fits=font=>{
  grid.style.setProperty('--overview-font',font+'px');
  return visible.every(card=>card.clientHeight>0&&card.scrollHeight<=card.clientHeight+1&&card.scrollWidth<=card.clientWidth+1);
 };
 if(!fits(minimum)){
  grid.classList.add('overview-scroll');grid.style.setProperty('--overview-font',(building?18:Math.min(goal,26))+'px');return;
 }
 let low=minimum,high=goal,best=minimum;
 while(low<=high){const middle=Math.floor((low+high)/2);if(fits(middle)){best=middle;low=middle+1}else{high=middle-1}}
 grid.style.setProperty('--overview-font',best+'px');
}
function scheduleInstructionBoardFit(){
 if(typeof window.requestAnimationFrame==='function'){
  if(overviewLayoutFrame!==null)window.cancelAnimationFrame(overviewLayoutFrame);
  overviewLayoutFrame=window.requestAnimationFrame(()=>{overviewLayoutFrame=null;fitInstructionBoard()});
 }else{fitInstructionBoard()}
}
function renderInstructionBoard(){
 const overview=instructionMode==='overview',fullBoard=overview||briefingComplete;
 const covered=[...revealedInstructions].filter(index=>index!==slideIndex).length;
 const building=!fullBoard&&covered>0;
 $('instructionSpotlight').hidden=fullBoard;$('instructionGrid').hidden=!(fullBoard||building);$('instructionNavigator').hidden=fullBoard;
 $('instructionGrid').classList.toggle('build-grid',building);$('instructionsPage').classList.toggle('building',building);
 $('instructionGrid').setAttribute('aria-label',fullBoard?'All quiz instructions':'Previously presented instructions');
 $('buildCaption').hidden=!building;$('buildCaptionText').textContent='Already covered · '+covered;
 overviewCards.forEach((card,index)=>{card.hidden=!fullBoard&&(!revealedInstructions.has(index)||index===slideIndex)});
 $('presentMode').classList.toggle('active',!overview);$('overviewMode').classList.toggle('active',overview);
 $('presentMode').setAttribute('aria-pressed',String(!overview));$('overviewMode').setAttribute('aria-pressed',String(overview));
 $('replayBriefing').hidden=!briefingComplete;
 $('shell').classList.toggle('overview-mode',currentPage==='instructions'&&fullBoard);
 $('slideCount').textContent=briefingComplete&&!overview?'All '+instructionSlides.length+' instructions · briefing complete':overview?'All '+instructionSlides.length+' instructions · select a card':'Instruction '+String(slideIndex+1).padStart(2,'0')+' of '+String(instructionSlides.length).padStart(2,'0');
 if(!$('instructionGrid').hidden)scheduleInstructionBoardFit();
}
function buildInstructionSlides(){
 c.instructions.forEach(item=>{if(item.text.trim())instructionSlides.push(item)});
 if(c.permittedMaterials)instructionSlides.push({title:'Permitted for this quiz',text:c.permittedMaterials,kind:'materials',label:'Materials',category:'YOUR APPROVED MATERIALS',tip:'Only bring the materials permitted for this assessment.'});
 c.extraComments.forEach((text,index)=>instructionSlides.push({title:c.extraComments.length===1?'One more thing…':'Additional instruction '+(index+1),text,kind:'extra',label:'Note '+(index+1),category:'PLEASE REMEMBER',tip:'If anything is unclear, ask the supervisor.'}));
 instructionSlides.push({title:'Protect the integrity of your work',text:c.integrityMessage,overviewTitle:'Academic integrity',overviewText:"Suspected cheating is recorded and reported under JCU's procedure. Follow staff directions. A warning does not prevent reporting. Penalties follow the University process.",kind:'integrity',label:'Integrity',category:'ACADEMIC INTEGRITY',tip:'Follow staff directions. Suspected cheating is recorded and reported.'});
 instructionSlides.forEach((item,index)=>{
  const card=document.createElement('button');card.type='button';card.className='instruction-card'+(item.kind==='integrity'?' wide-card integrity-note':item.kind==='materials'?' materials-note':item.kind==='extra'?' extra-comments':'');
  card.setAttribute('aria-label','Present instruction '+(index+1)+': '+item.title);card.style.setProperty('--card-order',Math.min(index,8));applySlidePalette(card,item,index);
  const art=document.createElement('div');art.className='card-icon';art.setAttribute('aria-hidden','true');art.innerHTML=instructionArt(item.kind);
  const header=document.createElement('div'),content=document.createElement('div'),category=document.createElement('div'),heading=document.createElement('h2'),copy=document.createElement('p');
  header.className='card-heading';category.className='card-category';category.textContent=String(index+1).padStart(2,'0')+' · '+item.label.toUpperCase();heading.className='card-title';heading.textContent=item.overviewTitle||item.title;copy.className='card-copy';emphasizeText(copy,item.overviewText||item.text);
  content.append(category,heading);header.append(art,content);card.append(header,copy);card.onclick=()=>{setInstructionMode('presentation');showInstructionSlide(index)};
  $('instructionGrid').append(card);overviewCards.push(card);
  const step=document.createElement('button');step.type='button';step.className='step-link';step.setAttribute('aria-label','Instruction '+(index+1)+': '+item.title);step.title=item.title;
  const digit=document.createElement('span'),label=document.createElement('span');digit.className='step-digit';digit.textContent=String(index+1).padStart(2,'0');label.className='step-label';label.textContent=item.label;step.append(digit,label);step.onclick=()=>showInstructionSlide(index);
  $('slideSteps').append(step);stepButtons.push(step);
 });
}
function updateAutoplayControls(){
 $('autoToggle').textContent=autoplay?'Ⅱ Pause':'▶ Auto-play';$('autoToggle').classList.toggle('playing',autoplay);$('autoToggle').setAttribute('aria-pressed',String(autoplay));
 if(!autoplay)$('autoStatus').textContent=slideIndex===instructionSlides.length-1?'Final instruction · Select ✓ to complete the board.':'Use ← → to navigate · P to play/pause';
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
 briefingComplete=false;
 slideIndex=Math.max(0,Math.min(instructionSlides.length-1,index));
 revealedInstructions.add(slideIndex);
 const item=instructionSlides[slideIndex],panel=$('instructionSpotlight');
 applySlidePalette(panel,item,slideIndex);$('slideArt').innerHTML=instructionArt(item.kind);
 $('slideCategory').textContent=String(slideIndex+1).padStart(2,'0')+' / '+item.category;$('slideTitle').textContent=item.title;emphasizeText($('slideBody'),item.text);$('slideTip').textContent=item.tip;
 $('slideCopy').scrollTop=0;panel.setAttribute('aria-label','Instruction '+(slideIndex+1)+' of '+instructionSlides.length+': '+item.title);
 stepButtons.forEach((step,i)=>{step.classList.toggle('active',i===slideIndex);step.setAttribute('aria-current',i===slideIndex?'step':'false')});
 $('previousInstruction').disabled=slideIndex===0;$('nextInstruction').disabled=false;
 const finalSlide=slideIndex===instructionSlides.length-1;$('nextInstruction').textContent=finalSlide?'✓':'→';$('nextInstruction').setAttribute('aria-label',finalSlide?'Show the completed instruction board':'Next instruction');
 panel.classList.remove('entering');void panel.offsetWidth;panel.classList.add('entering');
 const step=stepButtons[slideIndex];if(currentPage==='instructions'&&instructionMode==='presentation'&&typeof step.scrollIntoView==='function')step.scrollIntoView({block:'nearest',inline:'nearest',behavior:'auto'});
 if(autoplay)resetSlideReadingTime();updateAutoplayControls();renderInstructionBoard();
}
function setInstructionMode(mode){
 instructionMode=mode;if(mode==='overview')stopInstructionAutoplay();renderInstructionBoard();
}
function finishInstructionBuild(){
 stopInstructionAutoplay();briefingComplete=true;instructionSlides.forEach((_,index)=>revealedInstructions.add(index));renderInstructionBoard();
}
function nextInstructionSlide(){
 if(briefingComplete)return;
 if(slideIndex===instructionSlides.length-1)finishInstructionBuild();else showInstructionSlide(slideIndex+1);
}
function replayInstructionBuild(){
 stopInstructionAutoplay();briefingComplete=false;revealedInstructions.clear();instructionMode='presentation';showInstructionSlide(0,false);
}
function updateInstructionAutoplay(){
 if(!autoplay)return;if(currentPage!=='instructions'||instructionMode!=='presentation'||document.hidden){stopInstructionAutoplay();return}
 let remaining=Math.max(0,autoTarget-Date.now());
 if(remaining<=0){if(slideIndex===instructionSlides.length-1){finishInstructionBuild();return}showInstructionSlide(slideIndex+1,false);remaining=autoDuration}
 $('slideProgress').style.transform='scaleX('+Math.min(1,1-remaining/autoDuration)+')';$('autoStatus').textContent='Next instruction in '+Math.ceil(remaining/1000)+'s · P to pause';
}
function toggleInstructionAutoplay(){
 if(autoplay){stopInstructionAutoplay();return}
 if(currentPage!=='instructions')return;
 setInstructionMode('presentation');if(briefingComplete||slideIndex===instructionSlides.length-1)replayInstructionBuild();
 autoplay=true;resetSlideReadingTime();clearInterval(autoTimer);autoTimer=setInterval(updateInstructionAutoplay,100);updateAutoplayControls();updateInstructionAutoplay();
}
buildInstructionSlides();showInstructionSlide(0,false);
function showPage(page){
 currentPage=page;const instructions=page==='instructions',survey=page==='survey';
 if(!instructions)stopInstructionAutoplay();
 $('instructionsPage').hidden=!instructions;$('timerPage').hidden=page!=='timer';$('surveyPage').hidden=!survey;
 $('instructionFooter').hidden=!instructions;$('timerFooter').hidden=page!=='timer';$('surveyFooter').hidden=!survey;
 $('instructionsTab').classList.toggle('active',instructions);$('timerTab').classList.toggle('active',page==='timer');$('surveyTab').classList.toggle('active',survey);
 $('instructionsTab').setAttribute('aria-pressed',String(instructions));$('timerTab').setAttribute('aria-pressed',String(page==='timer'));$('surveyTab').setAttribute('aria-pressed',String(survey));
 $('shell').classList.toggle('instructions-mode',instructions);
 $('shell').classList.toggle('survey-mode',survey);
 $('subtitle').textContent=instructions?'A few simple steps before we begin':survey?'Please complete your subject survey in LearnJCU':c.subtitle;
 if(survey)updateSurveyReminder(true);
 renderInstructionBoard();render();saveTimer(true);requestAnimationFrame(fitTimer);
}
function fitTimer(){
 const stage=$('timerPage');if(stage.hidden)return;
 const css=getComputedStyle(stage);
 const w=stage.clientWidth-parseFloat(css.paddingLeft)-parseFloat(css.paddingRight)-24;
 const h=stage.clientHeight-parseFloat(css.paddingTop)-parseFloat(css.paddingBottom)-24;
 const size=Math.max(110,Math.min(w,h,document.fullscreenElement?760:590));
 stage.querySelector('.timer').style.setProperty('--timer-size',size+'px');
}
function fmt(s){s=Math.max(0,Math.round(s));let h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return h?`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`:`${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`}
function tone(f=650,d=.16){if(!c.sound)return;try{let a=new(AudioContext||webkitAudioContext),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=f;g.gain.setValueAtTime(.13,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d);o.start();o.stop(a.currentTime+d)}catch(e){}}
function announce(text,seconds=3){if(currentPage!=='timer')showPage('timer');clearTimeout(bannerTimer);$('banner').textContent=text;$('banner').classList.add('show');tone();if(seconds<3600)bannerTimer=setTimeout(()=>$('banner').classList.remove('show'),seconds*1000)}
function render(){
 const p=total?Math.max(0,Math.min(100,left/total*100)):0;
 const color=phase==='reading'?c.readingColour:!c.changeRingColour?c.ringColour:p<=c.red?c.redColour:p<=c.amber?c.amberColour:c.ringColour;
 document.body.style.setProperty('--ring-colour',color);document.body.style.setProperty('--ring-glow',color+'35');document.body.style.setProperty('--banner-border',color);
 $('ring').style.strokeDashoffset=L*(1-p/100);
 $('phase').textContent=ended?'FINISHED':phase==='reading'?'READING TIME':'WRITING TIME';$('clock').textContent=fmt(left);$('clock').classList.toggle('has-hours',Math.round(left)>=3600);
 $('pct').innerHTML='<strong>'+Math.ceil(p)+'%</strong><span class="pct-label">REMAINING</span>';
 $('elapsed').textContent='Elapsed '+fmt(elapsed);
 $('ring').classList.toggle('urgent',currentPage==='timer'&&phase==='exam'&&left>0&&left<=c.pulseMinutes*60&&running&&c.pulseStyle!=='Off'&&!prefersReducedMotion);
 $('start').textContent=ended?'Finished':running?'Running':'▶ '+(hasStarted?'Resume':'Start');$('start').disabled=running||ended;$('pause').disabled=!running;
 $('endScreen').classList.toggle('show',ended);$('endScreen').setAttribute('aria-hidden',String(!ended));
 $('endPlus5').disabled=locked;
 const status=ended?'Time expired · add time to continue':running?`${phase==='reading'?'Reading':'Writing'} · ${fmt(left)} remaining`:hasStarted?`Paused · ${fmt(left)} remaining`:'Timer ready';
 if($('pageStatus').textContent!==status)$('pageStatus').textContent=status;
 finishTime();
}
function finishTime(){
 if(!running&&!ended&&hasStarted){$('headerFinish').textContent='Paused · finish time updates on resume';return}
 const finish=ended?endedAt:(running?target:Date.now()+left*1000)+(phase==='reading'?plannedExam*1000:0);
 $('headerFinish').textContent=(ended?'Finished at: ':running?'Finish time: ':'Estimated finish: ')+new Date(finish).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
}
function clearNotice(){clearTimeout(bannerTimer);bannerTimer=null;$('banner').classList.remove('show')}
function expire(){
 endedAt=target||Date.now();left=0;elapsed=total;running=false;ended=true;hasStarted=true;
 clearInterval(timer);timer=null;clearNotice();
 if(currentPage!=='timer')showPage('timer');
 tone(420,.5);
}
function beginExam(overrun=0){
 phase='exam';total=plannedExam;left=Math.max(0,total-overrun);elapsed=total-left;said.clear();
 target=Date.now()+(total-overrun)*1000;
 if(left>0)announce('READING TIME ENDED — WRITING TIME STARTS NOW',4);
 else expire();
}
function tick(){
 if(!running)return;
 const previous=left,now=Date.now();left=Math.max(0,(target-now)/1000);elapsed=Math.max(0,total-left);
 if(left<=0){
  if(phase==='reading')beginExam(Math.max(0,(now-target)/1000));else expire();
 }else if(phase==='exam'){
  // A background tab may cross several warnings. Show only the nearest one.
  const crossed=c.milestones.filter(m=>previous>m*60&&left<=m*60&&!said.has(m));
  crossed.forEach(m=>said.add(m));
  if(crossed.length){const m=Math.min(...crossed);announce(`${m} minute${m===1?'':'s'} remaining`)}
 }
 render();saveTimer();
}
function collapseSidebar(){if(!c.collapseSidebar)return;try{const b=window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"] button');if(b)b.click()}catch(e){}}
function start(){if(!running&&!ended&&left>0){running=true;hasStarted=true;target=Date.now()+left*1000;clearInterval(timer);timer=setInterval(tick,200);render();saveTimer(true);collapseSidebar()}}
function pause(){if(running){tick();if(!ended)running=false;clearInterval(timer);timer=null;render();saveTimer(true)}}
function reset(){
 if(locked)return;
 if(!window.confirm('Reset the timer and use the durations currently selected in Timer setup?'))return;
 running=false;ended=false;hasStarted=false;endedAt=0;target=0;plannedExam=c.exam;
 clearInterval(timer);timer=null;clearNotice();clearTimeout(feedbackTimer);$('timeFeedback').textContent='';
 phase=c.reading?'reading':'exam';total=c.reading||c.exam;left=total;elapsed=0;said.clear();
 try{sessionStorage.removeItem(storageKey)}catch(e){}
 render();
}
function feedback(text){clearTimeout(feedbackTimer);$('timeFeedback').textContent=text;feedbackTimer=setTimeout(()=>$('timeFeedback').textContent='',7000)}
function adjust(seconds){
 if(locked||!Number.isFinite(seconds)||seconds===0)return;
 // Synchronise with the deadline first, so a late click never revives stale seconds.
 if(running)tick();
 const wasEnded=ended,previousLeft=left;
 left=Math.max(0,left+seconds);const change=left-previousLeft;
 if(change===0){feedback('No time remaining to subtract.');return}
 // Adding or removing time changes the allocation, never the elapsed time.
 total=elapsed+left;
 c.milestones.forEach(m=>{if(left>m*60)said.delete(m)});
 clearNotice();
 if(left>0){
  if(wasEnded){
   ended=false;endedAt=0;running=true;hasStarted=true;
   clearInterval(timer);timer=setInterval(tick,200);
  }
  if(running)target=Date.now()+left*1000;
 }else if(phase==='reading')beginExam();else{target=Date.now();expire()}
 const minutes=Math.round(Math.abs(change)/60*100)/100;
 feedback((change>0?'Added ':'Removed ')+minutes+' min'+(wasEnded&&change>0?' · countdown resumed.':'.'));
 render();saveTimer(true);
}
function customAdjust(direction){
 if(locked)return;
 const input=$('adjustMinutes');
 if(!input.checkValidity()||!input.value){input.reportValidity();return}
 adjust(direction*Number(input.value)*60);
}
function manualWarning(text,seconds=5){announce(text,seconds)}
function renderLock(){
 ['plus','plus5','plus10','minus','minus5','customPlus','customMinus','adjustMinutes','endPlus5','reset'].forEach(id=>$(id).disabled=locked);
 $('lock').textContent=locked?'🔓 Unlock':'🔒 Lock';$('lock').classList.toggle('lock-active',locked);
}
function toggleLock(){locked=!locked;renderLock();saveTimer(true)}
function saveTimer(force=false){
 if(!hasStarted)return;
 const now=Date.now();if(!force&&now-lastSavedAt<1000)return;lastSavedAt=now;
 try{sessionStorage.setItem(storageKey,JSON.stringify({version:3,setupReading:c.reading,setupExam:c.exam,phase,total,left,elapsed,running,ended,target,endedAt,plannedExam,locked,said:[...said],page:currentPage}))}catch(e){}
}
function restoreTimer(){
 try{
  const state=JSON.parse(sessionStorage.getItem(storageKey)||'null');
  if(!state||state.version!==3||!['reading','exam'].includes(state.phase))return;
  // Appearance changes retain a live timer. Duration changes must take effect now.
  if(state.setupReading!==c.reading||state.setupExam!==c.exam){
   sessionStorage.removeItem(storageKey);currentPage='timer';
   feedback('New durations applied · ready to start.');return;
  }
  if(!['total','left','elapsed','target','endedAt','plannedExam'].every(k=>Number.isFinite(state[k])&&state[k]>=0)||state.plannedExam<=0||state.left>state.total)return;
  if((state.running&&state.ended)||(state.running&&state.target<=0))return;
  ({phase,total,left,elapsed,running,ended,target,endedAt,plannedExam,locked}=state);
  said=new Set(Array.isArray(state.said)?state.said:[]);hasStarted=true;
  if(['instructions','timer','survey'].includes(state.page))currentPage=state.page;
  renderLock();
 }catch(e){}
}
$('start').onclick=start;$('pause').onclick=pause;$('reset').onclick=reset;
$('plus').onclick=()=>adjust(60);$('plus5').onclick=()=>adjust(300);$('plus10').onclick=()=>adjust(600);$('minus').onclick=()=>adjust(-60);$('minus5').onclick=()=>adjust(-300);
$('customPlus').onclick=()=>customAdjust(1);$('customMinus').onclick=()=>customAdjust(-1);$('endPlus5').onclick=()=>adjust(300);
$('warn15').onclick=()=>manualWarning('⚠ 15 MINUTES REMAINING',5);$('warn5').onclick=()=>manualWarning('⚠ 5 MINUTES REMAINING',5);$('stopmsg').onclick=()=>manualWarning('STOP WRITING NOW',8);$('lock').onclick=toggleLock;
async function toggleFullscreen(){try{if(document.fullscreenElement){await document.exitFullscreen()}else{await $('shell').requestFullscreen()}}catch(e){console.warn('Full screen is unavailable in this browser. Use the browser full-screen option instead.')}}
$('full').onclick=toggleFullscreen;$('instructionsFull').onclick=toggleFullscreen;$('surveyFull').onclick=toggleFullscreen;
$('instructionsTab').onclick=()=>showPage('instructions');$('timerTab').onclick=()=>showPage('timer');$('showTimer').onclick=()=>showPage('timer');
$('surveyTab').onclick=()=>showPage('survey');$('surveyTimer').onclick=()=>showPage('timer');
$('presentMode').onclick=()=>setInstructionMode('presentation');$('overviewMode').onclick=()=>setInstructionMode('overview');$('autoToggle').onclick=toggleInstructionAutoplay;
$('previousInstruction').onclick=()=>showInstructionSlide(slideIndex-1);$('nextInstruction').onclick=nextInstructionSlide;$('replayBriefing').onclick=replayInstructionBuild;
document.addEventListener('visibilitychange',()=>{if(document.hidden){stopInstructionAutoplay();saveTimer(true)}else if(running)tick()});
window.addEventListener('pagehide',()=>saveTimer(true));
document.addEventListener('fullscreenchange',scheduleInstructionBoardFit);
document.addEventListener('fullscreenchange',fitTimer);
window.addEventListener('resize',fitTimer);
if(typeof window.addEventListener==='function')window.addEventListener('resize',scheduleInstructionBoardFit);
if(typeof ResizeObserver==='function'){const boardObserver=new ResizeObserver(scheduleInstructionBoardFit);boardObserver.observe($('instructionGrid'));boardObserver.observe($('instructionsPage'))}
if(typeof ResizeObserver==='function'){const timerObserver=new ResizeObserver(fitTimer);timerObserver.observe($('timerPage'))}
document.querySelectorAll('.controls').forEach(control=>control.classList.add('controls-visible'));
document.addEventListener('keydown',e=>{
 if(e.repeat||e.ctrlKey||e.metaKey||e.altKey||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
 const key=e.key.toLowerCase();
 if(key==='i')showPage('instructions');if(key==='t')showPage('timer');if(key==='s')showPage('survey');if(key==='f')toggleFullscreen();
 if(currentPage==='instructions'){
  if(e.key==='ArrowRight'){e.preventDefault();setInstructionMode('presentation');nextInstructionSlide()}
  if(e.key==='ArrowLeft'){e.preventDefault();setInstructionMode('presentation');showInstructionSlide(slideIndex-1)}
  if(e.key==='Home'){e.preventDefault();setInstructionMode('presentation');showInstructionSlide(0)}
  if(e.key==='End'){e.preventDefault();setInstructionMode('presentation');showInstructionSlide(instructionSlides.length-1)}
  if(key==='p')toggleInstructionAutoplay();if(key==='o')setInstructionMode(instructionMode==='overview'?'presentation':'overview');
 }
 if(currentPage==='timer'){
  if(e.code==='Space'){e.preventDefault();running?pause():start()}
  if(key==='r')reset();if(key==='l')toggleLock();
  if(e.key==='+'||e.key==='='){e.preventDefault();adjust(60)}
  if(e.key==='-'){e.preventDefault();adjust(-60)}
 }
});
restoreTimer();showPage(currentPage);
if(running){tick();if(running)timer=setInterval(tick,200)}
if(c.instructionAutoplay&&currentPage==='instructions'&&instructionMode==='presentation')toggleInstructionAutoplay();
</script>
</body>
</html>""".replace("__CONFIG__", config_json)

st.caption("Projector preview • Build the instruction board as you present, show all instructions, or open the subject survey reminder. Switching pages preserves the countdown.")
components.html(html, height=820, scrolling=False)
with st.expander("Keyboard controls"):
    st.write(
        "**I:** instructions  |  **T:** timer  |  **S:** subject survey  |  **F:** full screen  |  "
        "**← / →:** previous/next instruction  |  **P:** play/pause instructions  |  "
        "**O:** presentation/overview  |  **Home / End:** first/last instruction  |  "
        "**Space:** start/pause on the timer page  |  "
        "**+ / −:** add/subtract one minute on the timer page  |  "
        "**R:** reset on the timer page  |  **L:** lock/unlock on the timer page"
    )
with st.expander("Subject survey access"):
    st.markdown(
        "Students can open **LearnJCU → Tools → YourJCU Survey Portal** and "
        "select the available survey for their subject. Use the sidebar to "
        "enter the current completed response count and total number of students. "
        "If the counts are not set or are invalid, the dial does not show a percentage.\n\n"
        f"[JCU student survey guide]({JCU_SURVEY_GUIDE_URL})"
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

