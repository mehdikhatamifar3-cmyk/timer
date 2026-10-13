import json
import streamlit as st
import streamlit.components.v1 as components

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
[data-testid="stSidebar"] div[data-baseweb="select"]>div {background:#fff!important;border-color:#b9c7da!important;}
[data-testid="stSidebar"] div[data-baseweb="select"] span,[data-testid="stSidebar"] div[data-baseweb="select"] svg {color:#102038!important;fill:#102038!important;}
[data-testid="stSidebar"] [data-testid="stSlider"] div,[data-testid="stSidebar"] [data-testid="stSlider"] span {color:#fff!important;}
[data-testid="stSidebarCollapseButton"] button,[data-testid="stSidebarCollapseButton"] svg {color:#fff!important;fill:#fff!important;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("ExamTimer Pro")
    st.caption("Configure, then launch the projector display.")
    title = st.text_input("Exam or subject title", "ME3512 Examination")
    subtitle = st.text_input("Subtitle", "Please manage your time carefully")

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
        ["Midnight", "Light", "Slate", "Ocean", "Forest", "High Contrast", "Warm Sand"],
    )
    show_logo = st.toggle("Show subtle JCU shield", True)

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
    "logo": "https://www.jcu.edu.au/__data/assets/image/0017/2322521/JCU-Logo-Shield-RGB-copy.png",
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
 --button-text:#f5f8ff;--primary-text:#06130c;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;font-family:Inter,Segoe UI,Arial,sans-serif;background:var(--bg);color:var(--text)}
body.light{--bg:#edf3fb;--panel:#fff;--text:#102038;--muted:#52637b;--track:#d5dfeb;--banner-bg:#102038;--banner-text:#fff;--button-text:#102038}
body.slate{--bg:#171a21;--panel:#242936;--text:#f7f8fb;--muted:#b8bfcc;--track:#3b4353;--banner-bg:#f7f8fb;--banner-text:#171a21}
body.ocean{--bg:#041b2d;--panel:#0a3048;--text:#f2fbff;--muted:#abd0df;--track:#1d526b;--banner-bg:#eefbff;--banner-text:#04243a}
body.forest{--bg:#071c16;--panel:#103128;--text:#f2fff9;--muted:#acd3c3;--track:#285848;--banner-bg:#f1fff8;--banner-text:#0a2b20}
body.contrast{--bg:#000;--panel:#111;--text:#fff;--muted:#fff;--track:#555;--banner-bg:#fff200;--banner-text:#000;--button-text:#fff}
body.sand{--bg:#f3ead8;--panel:#fffaf0;--text:#3a2a1e;--muted:#705b48;--track:#d7c4a5;--banner-bg:#342519;--banner-text:#fff8e9;--button-text:#3a2a1e}
.shell{height:100vh;min-height:640px;padding:24px;display:grid;grid-template-rows:auto 1fr auto;background:radial-gradient(circle at 50% 42%,var(--glow),transparent 34%),var(--bg);transition:.4s}
header{text-align:center;position:relative}.logo{position:absolute;left:6px;top:3px;height:62px;max-width:92px;object-fit:contain;opacity:.30;filter:saturate(.65);transition:.25s}
.title{font-size:clamp(27px,3vw,48px);font-weight:900}.subtitle{font-size:clamp(14px,1.4vw,22px);color:var(--muted);margin-top:5px}
.stage{display:grid;place-items:center;position:relative}.timer{width:min(65vh,660px);height:min(65vh,660px);min-width:380px;min-height:380px;position:relative;display:grid;place-items:center;perspective:1000px}
.disc{position:absolute;inset:8%;border-radius:50%;background:radial-gradient(circle at 50% 34%,rgba(255,255,255,.14),transparent 25%),var(--panel);box-shadow:0 38px 75px #0008,inset 0 8px 16px #fff1,inset 0 -22px 40px #0006;transform:rotateX(7deg)}
svg{position:absolute;width:100%;height:100%;transform:rotate(-90deg);filter:drop-shadow(0 0 17px var(--glow))}.track,.progress{fill:none;stroke-width:22}.track{stroke:var(--track)}.progress{stroke:var(--accent);stroke-linecap:round;transition:.3s}
.content{z-index:2;text-align:center}.phase{font-size:clamp(17px,1.7vw,25px);font-weight:900;letter-spacing:3px;color:var(--accent)}.clock{font-size:clamp(68px,8.5vw,135px);font-weight:950;letter-spacing:-5px;font-variant-numeric:tabular-nums;text-shadow:0 8px 26px #0007}.pct{font-size:clamp(16px,1.5vw,23px);color:var(--muted);font-weight:700}
.banner{position:absolute;z-index:4;width:min(92%,900px);padding:30px 38px;border:3px solid var(--banner-border);border-radius:24px;background:var(--banner-bg);color:var(--banner-text);text-align:center;font-size:clamp(28px,4vw,57px);font-weight:950;line-height:1.15;letter-spacing:.3px;box-shadow:0 25px 80px #000b,0 0 35px var(--glow);opacity:0;transform:scale(.85);pointer-events:none;transition:.25s}.banner.show{opacity:1;transform:scale(1)}
footer{text-align:center}.meta{color:var(--muted);margin:0 0 10px}.controls{display:flex;flex-wrap:wrap;justify-content:center;gap:9px}.controls button{padding:12px 19px;border-radius:13px;border:1px solid #ffffff30;background:var(--panel);color:var(--button-text);font-size:16px;font-weight:850;cursor:pointer;box-shadow:0 8px 20px #0004}.controls .primary{background:var(--accent);color:var(--primary-text)}.flash{animation:flash .8s infinite}@keyframes flash{50%{filter:brightness(1.6)}}
.shell:fullscreen{padding:clamp(18px,2vw,42px)}.shell:fullscreen .timer{width:min(78vh,78vw);height:min(78vh,78vw);max-width:900px;max-height:900px}.shell:fullscreen .clock{font-size:clamp(100px,12vw,210px)}.shell:fullscreen .phase{font-size:clamp(24px,2.5vw,40px)}.shell:fullscreen .pct{font-size:clamp(20px,2vw,32px)}.shell:fullscreen .title{font-size:clamp(38px,4vw,72px)}.shell:fullscreen .subtitle{font-size:clamp(18px,1.8vw,30px)}.shell:fullscreen .logo{height:clamp(65px,8vh,105px);max-width:140px;opacity:.25}.shell:fullscreen .banner{font-size:clamp(42px,5vw,82px);padding:42px}
@media(max-width:650px){.shell{padding:12px}.timer{min-width:320px;min-height:320px;width:min(60vh,92vw);height:min(60vh,92vw)}.logo{height:42px}.clock{letter-spacing:-2px}.banner{padding:22px 18px}}
</style>
</head>
<body>
<div class="shell" id="shell">
<header><img class="logo" id="logo"><div class="title" id="title"></div><div class="subtitle" id="subtitle"></div></header>
<main class="stage">
<div class="timer"><div class="disc"></div><svg viewBox="0 0 420 420"><circle class="track" cx="210" cy="210" r="180"/><circle class="progress" id="ring" cx="210" cy="210" r="180"/></svg><div class="content"><div class="phase" id="phase">READY</div><div class="clock" id="clock"></div><div class="pct" id="pct"></div></div></div>
<div class="banner" id="banner"></div>
</main>
<footer><div class="meta"><span id="elapsed"></span> · <span id="finish">Finish time: --:--</span></div><div class="controls"><button class="primary" id="start">▶ Start</button><button id="pause">Ⅱ Pause</button><button id="plus">+ 1 min</button><button id="minus">− 1 min</button><button id="reset">↺ Reset</button><button id="full">⛶ Full Screen</button></div></footer>
</div>
<script>
const c=__CONFIG__,$=id=>document.getElementById(id);
const themeClasses={Light:'light',Slate:'slate',Ocean:'ocean',Forest:'forest','High Contrast':'contrast','Warm Sand':'sand'};
if(themeClasses[c.theme])document.body.classList.add(themeClasses[c.theme]);
$('title').textContent=c.title;$('subtitle').textContent=c.subtitle;
if(c.showLogo){$('logo').src=c.logo}else{$('logo').style.display='none'}
const L=2*Math.PI*180;$('ring').style.strokeDasharray=L;
let phase=c.reading?'reading':'exam',total=c.reading||c.exam,left=total,elapsed=0,running=false,ended=false,target=0,timer=null,said=new Set(),bannerTimer=null;
function fmt(s){s=Math.max(0,Math.round(s));let h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return h?`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`:`${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`}
function tone(f=650,d=.16){if(!c.sound)return;try{let a=new(AudioContext||webkitAudioContext),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=f;g.gain.setValueAtTime(.13,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d);o.start();o.stop(a.currentTime+d)}catch(e){}}
function announce(text,seconds=3){clearTimeout(bannerTimer);$('banner').textContent=text;$('banner').classList.add('show');tone();if(seconds<3600)bannerTimer=setTimeout(()=>$('banner').classList.remove('show'),seconds*1000)}
function render(){let p=total?Math.max(0,left/total*100):0,color=p<=c.red?'#ff4d5e':p<=c.amber?'#ffb020':'#2ed47a';document.documentElement.style.setProperty('--accent',color);document.documentElement.style.setProperty('--glow',color+'66');document.documentElement.style.setProperty('--banner-border',color);$('ring').style.strokeDashoffset=L*(1-p/100);$('phase').textContent=ended?'FINISHED':phase==='reading'?'READING TIME':'WRITING TIME';$('clock').textContent=fmt(left);$('pct').textContent=Math.ceil(p)+'% remaining';$('elapsed').textContent='Elapsed '+fmt(elapsed);$('shell').classList.toggle('flash',p<=c.flash&&running);$('start').textContent=running?'Running':'▶ '+(elapsed?'Resume':'Start')}
function finishTime(){let d=new Date(Date.now()+left*1000+(phase==='reading'?c.exam*1000:0));$('finish').textContent='Finish time: '+d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}
function tick(){if(!running)return;let previous=left;left=Math.max(0,(target-Date.now())/1000);elapsed=total-left;if(phase==='exam')c.milestones.forEach(m=>{if(previous>m*60&&left<=m*60&&!said.has(m)){said.add(m);announce(`${m} minute${m===1?'':'s'} remaining`)}});if(left<=0){if(phase==='reading'){phase='exam';total=c.exam;left=total;elapsed=0;target=Date.now()+left*1000;said.clear();announce('READING TIME ENDED — WRITING TIME STARTS NOW',4);finishTime()}else{running=false;ended=true;clearInterval(timer);announce(c.endMessage,86400);tone(420,.5)}}render()}
function start(){if(!running&&!ended){running=true;target=Date.now()+left*1000;timer=setInterval(tick,200);finishTime();render()}}
function pause(){if(running){tick();running=false;clearInterval(timer);render()}}
function reset(){running=false;ended=false;clearInterval(timer);clearTimeout(bannerTimer);phase=c.reading?'reading':'exam';total=c.reading||c.exam;left=total;elapsed=0;said.clear();$('banner').classList.remove('show');$('finish').textContent='Finish time: --:--';render()}
function adjust(seconds){left=Math.max(0,left+seconds);total=Math.max(total,left);if(running)target=Date.now()+left*1000;finishTime();render()}
$('start').onclick=start;$('pause').onclick=pause;$('reset').onclick=reset;$('plus').onclick=()=>adjust(60);$('minus').onclick=()=>adjust(-60);$('full').onclick=()=>document.fullscreenElement?document.exitFullscreen():$('shell').requestFullscreen();
document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();running?pause():start()}if(e.key.toLowerCase()==='r')reset();if(e.key.toLowerCase()==='f')$('full').click()});
render();
</script>
</body>
</html>""".replace("__CONFIG__", config_json)

st.caption("Projector display preview")
components.html(html, height=820, scrolling=False)
with st.expander("Keyboard controls"):
    st.write("**Space:** start/pause  |  **F:** full screen  |  **R:** reset")

