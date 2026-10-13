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
.shell{height:100vh;min-height:640px;padding:18px 24px;display:grid;grid-template-rows:auto minmax(0,1fr) auto;background:radial-gradient(circle at 50% 42%,var(--glow),transparent 34%),var(--bg);transition:.4s}
header{text-align:center;position:relative}.logo{position:absolute;left:6px;top:3px;height:62px;max-width:92px;object-fit:contain;opacity:.30;filter:saturate(.65);transition:.25s}
.title{font-size:clamp(27px,3vw,48px);font-weight:900}.subtitle{font-size:clamp(14px,1.4vw,22px);color:var(--muted);margin-top:5px}.header-finish{font-size:clamp(13px,1.15vw,18px);color:var(--muted);font-weight:750;margin-top:7px}
.stage{display:grid;place-items:center;position:relative;overflow:visible;min-height:0;padding:18px 30px}.timer{width:min(57vh,590px);height:min(57vh,590px);min-width:350px;min-height:350px;position:relative;display:grid;place-items:center;perspective:1000px;overflow:visible;margin:12px}
.disc{position:absolute;inset:8%;border-radius:50%;background:radial-gradient(circle at 50% 34%,rgba(255,255,255,.14),transparent 25%),var(--panel);box-shadow:0 38px 75px #0008,inset 0 8px 16px #fff1,inset 0 -22px 40px #0006;transform:rotateX(7deg)}
svg{position:absolute;inset:-9%;width:118%;height:118%;padding:9%;overflow:visible;transform:rotate(-90deg);filter:none}.track,.progress{fill:none;stroke-width:22}.track{stroke:var(--track)}.progress{stroke:var(--accent);stroke-linecap:round;transition:stroke .3s,stroke-width .45s,stroke-dashoffset .3s;filter:drop-shadow(0 0 8px var(--accent)) drop-shadow(0 0 15px var(--glow));animation:ringBreathe 8s ease-in-out infinite;will-change:filter}@keyframes ringBreathe{0%,100%{filter:drop-shadow(0 0 7px var(--accent)) drop-shadow(0 0 12px var(--glow))}50%{filter:drop-shadow(0 0 12px var(--accent)) drop-shadow(0 0 24px var(--glow))}}
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
<main class="stage">
<div class="timer"><div class="disc"></div><div class="markers"><span class="marker m75" title="75%"></span><span class="marker m50" title="50%"></span><span class="marker m25" title="25%"></span><span class="marker m10" title="10%"></span></div><svg viewBox="0 0 420 420"><circle class="track" cx="210" cy="210" r="180"/><circle class="progress" id="ring" cx="210" cy="210" r="180"/></svg><div class="content"><div class="phase" id="phase">READY</div><div class="clock" id="clock"></div><div class="pct" id="pct"></div></div></div>
<div class="banner" id="banner"></div><div class="end-screen" id="endScreen"><div class="end-line"></div><div class="end-main">TIME EXPIRED</div><div class="end-sub">STOP WRITING NOW</div><div class="end-line"></div></div>
</main>
<footer><div class="meta"><span id="elapsed"></span></div><div class="controls"><button class="primary" id="start">▶ Start</button><button id="pause">Ⅱ Pause</button><button id="plus">+ 1 min</button><button id="plus5">+ 5 min</button><button id="plus10">+ 10 min</button><button id="minus">− 1 min</button><button id="reset">↺ Reset</button><button id="warn15">⚠ 15 min</button><button id="warn5">⚠ 5 min</button><button id="stopmsg">■ Stop Writing</button><button id="lock">🔒 Lock Controls</button><button id="full">⛶ Full Screen</button></div></footer>
</div>
<script>
const c=__CONFIG__,$=id=>document.getElementById(id);
const themeClasses={Light:'light',Slate:'slate',Ocean:'ocean',Forest:'forest','High Contrast':'contrast','Warm Sand':'sand','JCU Blue & Gold':'jcu','Engineering Graphite':'engineering','Examination White':'examwhite','Lecture Blue':'lecture'};
if(themeClasses[c.theme])document.body.classList.add(themeClasses[c.theme]);
$('title').textContent=c.title;$('subtitle').textContent=c.subtitle;
if(c.showLogo){$('logo').src=c.logo}else{$('logo').style.display='none'}
const L=2*Math.PI*180;$('ring').style.strokeDasharray=L;
let phase=c.reading?'reading':'exam',total=c.reading||c.exam,left=total,elapsed=0,running=false,ended=false,target=0,timer=null,said=new Set(),bannerTimer=null,locked=false;
function fmt(s){s=Math.max(0,Math.round(s));let h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return h?`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`:`${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`}
function tone(f=650,d=.16){if(!c.sound)return;try{let a=new(AudioContext||webkitAudioContext),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=f;g.gain.setValueAtTime(.13,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d);o.start();o.stop(a.currentTime+d)}catch(e){}}
function announce(text,seconds=3){clearTimeout(bannerTimer);$('banner').textContent=text;$('banner').classList.add('show');tone();if(seconds<3600)bannerTimer=setTimeout(()=>$('banner').classList.remove('show'),seconds*1000)}
function render(){let p=total?Math.max(0,left/total*100):0,color=phase==='reading'?'#2f8cff':p<=c.red?'#ff4d5e':p<=c.amber?'#ffb020':'#2ed47a',thickness=p<=c.flash?34:p<=c.red?29:p<=c.amber?25:22;document.documentElement.style.setProperty('--accent',color);document.documentElement.style.setProperty('--glow',color+'66');document.documentElement.style.setProperty('--banner-border',color);$('ring').style.strokeDashoffset=L*(1-p/100);$('ring').style.strokeWidth=thickness;$('phase').textContent=ended?'FINISHED':phase==='reading'?'📖 READING TIME':'✍ WRITING TIME';$('clock').textContent=fmt(left);$('pct').innerHTML='<strong>'+Math.ceil(p)+'%</strong><br><span style="font-size:.72em;letter-spacing:2px">REMAINING</span>';$('elapsed').textContent='Elapsed '+fmt(elapsed);$('shell').classList.toggle('flash',p<=c.flash&&running);$('start').textContent=running?'Running':'▶ '+(elapsed?'Resume':'Start');$('endScreen').classList.toggle('show',ended)}
function finishTime(){let d=new Date(Date.now()+left*1000+(phase==='reading'?c.exam*1000:0));$('headerFinish').textContent='Finish time: '+d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}
function tick(){if(!running)return;let previous=left;left=Math.max(0,(target-Date.now())/1000);elapsed=total-left;if(phase==='exam')c.milestones.forEach(m=>{if(previous>m*60&&left<=m*60&&!said.has(m)){said.add(m);announce(`${m} minute${m===1?'':'s'} remaining`)}});if(left<=0){if(phase==='reading'){phase='exam';total=c.exam;left=total;elapsed=0;target=Date.now()+left*1000;said.clear();announce('READING TIME ENDED — WRITING TIME STARTS NOW',4);finishTime()}else{running=false;ended=true;clearInterval(timer);announce(c.endMessage,86400);tone(420,.5)}}render()}
function collapseSidebar(){if(!c.collapseSidebar)return;try{const b=window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"] button');if(b)b.click()}catch(e){}}
function start(){if(!running&&!ended){running=true;target=Date.now()+left*1000;timer=setInterval(tick,200);finishTime();render();collapseSidebar()}}
function pause(){if(running){tick();running=false;clearInterval(timer);render()}}
function reset(){if(locked)return;const ok=window.confirm('Reset the timer and return to the initial reading/exam time?');if(!ok)return;running=false;ended=false;clearInterval(timer);clearTimeout(bannerTimer);phase=c.reading?'reading':'exam';total=c.reading||c.exam;left=total;elapsed=0;said.clear();$('banner').classList.remove('show');$('headerFinish').textContent='Finish time: --:--';render()}
function adjust(seconds){if(locked)return;left=Math.max(0,left+seconds);total=Math.max(total,left);if(running)target=Date.now()+left*1000;finishTime();render()}
function manualWarning(text,seconds=5){announce(text,seconds)}
function toggleLock(){locked=!locked;['plus','plus5','plus10','minus','reset'].forEach(id=>$(id).disabled=locked);$('lock').textContent=locked?'🔓 Unlock Controls':'🔒 Lock Controls';$('lock').classList.toggle('lock-active',locked)}
$('start').onclick=start;$('pause').onclick=pause;$('reset').onclick=reset;$('plus').onclick=()=>adjust(60);$('plus5').onclick=()=>adjust(300);$('plus10').onclick=()=>adjust(600);$('minus').onclick=()=>adjust(-60);$('warn15').onclick=()=>manualWarning('⚠ 15 MINUTES REMAINING',5);$('warn5').onclick=()=>manualWarning('⚠ 5 MINUTES REMAINING',5);$('stopmsg').onclick=()=>manualWarning('STOP WRITING NOW',8);$('lock').onclick=toggleLock;$('full').onclick=()=>document.fullscreenElement?document.exitFullscreen():$('shell').requestFullscreen();
const controls=document.querySelector('.controls');controls.classList.add('controls-visible');
document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();running?pause():start()}if(e.key.toLowerCase()==='r')reset();if(e.key.toLowerCase()==='l')toggleLock();if(e.key.toLowerCase()==='f')$('full').click()});
controls.classList.add('controls-visible');render();
</script>
</body>
</html>""".replace("__CONFIG__", config_json)

st.caption("Projector display preview")
components.html(html, height=820, scrolling=False)
with st.expander("Keyboard controls"):
    st.write("**Space:** start/pause  |  **F:** full screen  |  **R:** reset  |  **L:** lock/unlock controls")
