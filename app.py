import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="FluoroLab | Fluorescence Spectroscopy",
    page_icon="🔬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d25 0%, #101b3c 55%, #102c42 100%);
    color: #f4f7ff;
}
.block-container {padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1200px;}
h1, h2, h3 {color: #f7fbff !important;}
p, li, label {color: #dce7ff;}
.hero {
    padding: 1.5rem; border-radius: 20px;
    background: linear-gradient(120deg, rgba(20,184,220,.18), rgba(139,92,246,.20));
    border: 1px solid rgba(125,211,252,.35);
}
.small-note {color:#b8c9e8; font-size:.9rem;}
.metric-card {
    padding: 1rem; border-radius: 14px; background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.12); min-height: 95px;
}
div[data-testid="stMetricValue"] {color:#67e8f9;}
.stTabs [data-baseweb="tab"] {color:#dce7ff;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🔬 FluoroLab 2.0</h1>
  <h3>Interactive Fluorescence Spectroscopy Simulator</h3>
  <p>Explore how a molecule absorbs light and emits fluorescence at a longer wavelength.</p>
  <p class="small-note">Engineering Chemistry · Unit II · Educational simulation</p>
</div>
""", unsafe_allow_html=True)

def fluorescence_animation():
    html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{box-sizing:border-box}
body{margin:0;background:#09132f;color:#eef5ff;font-family:Arial,sans-serif}
.panel{border:1px solid #28558c;border-radius:18px;overflow:hidden;background:
radial-gradient(circle at 50% 48%,rgba(26,80,150,.25),transparent 48%),#09132f}
.top{padding:15px 17px 4px;font-size:20px;font-weight:700}
.sub{padding:0 17px 8px;color:#b9cbed;font-size:13px}
canvas{display:block;width:100%;height:310px;touch-action:pan-y}
.status{padding:10px 16px;color:#aeeeff;font-weight:700;min-height:38px}
.controls{display:flex;gap:9px;padding:0 15px 15px;flex-wrap:wrap}
button{border:0;border-radius:10px;padding:10px 16px;font-weight:700;cursor:pointer}
#play{background:#22d3ee;color:#062238}
#pause{background:#334b78;color:white}
#replay{background:#8b5cf6;color:white}
.legend{display:flex;gap:14px;flex-wrap:wrap;padding:0 16px 14px;color:#cbdaf4;font-size:12px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
</style>
</head>
<body>
<div class="panel">
 <div class="top">✨ Watch fluorescence happen automatically</div>
 <div class="sub">The animation repeats the four stages. No dragging is needed.</div>
 <canvas id="scene"></canvas>
 <div class="status" id="status">Stage 1 · Excitation photon approaches the molecule</div>
 <div class="controls">
  <button id="play">▶ Play</button>
  <button id="pause">Ⅱ Pause</button>
  <button id="replay">↻ Replay</button>
 </div>
 <div class="legend">
  <span><i class="dot" style="background:#ffe45c"></i>Excitation photon</span>
  <span><i class="dot" style="background:#d78cff"></i>Excited molecule</span>
  <span><i class="dot" style="background:#55e8ff"></i>Emitted photon</span>
 </div>
</div>
<script>
const canvas=document.getElementById('scene');
const ctx=canvas.getContext('2d');
const statusEl=document.getElementById('status');
let W=700,H=310,dpr=1,elapsed=0,playing=true,last=0;
const duration=10;
function resize(){
 const r=canvas.getBoundingClientRect(); dpr=Math.min(window.devicePixelRatio||1,2);
 W=Math.max(320,r.width); H=310;
 canvas.width=Math.round(W*dpr); canvas.height=Math.round(H*dpr);
 ctx.setTransform(dpr,0,0,dpr,0,0);
}
new ResizeObserver(resize).observe(canvas); resize();
function clamp(x,a,b){return Math.max(a,Math.min(b,x))}
function smooth(x){x=clamp(x,0,1);return x*x*(3-2*x)}
function line(x1,y1,x2,y2,color,width=3){
 ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke();
}
function glowCircle(x,y,r,color,blur=18){
 ctx.save();ctx.shadowBlur=blur;ctx.shadowColor=color;ctx.fillStyle=color;
 ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.restore();
}
function drawPhoton(x,y,color,label){
 glowCircle(x,y,8,color,22);
 ctx.fillStyle=color;ctx.font='bold 12px Arial';ctx.fillText(label,x-35,y-18);
}
function drawMolecule(t,excited){
 const x=W*.52,y=H*.53;
 const pulse=excited?(1+0.09*Math.sin(t*9)):1;
 ctx.save();
 ctx.shadowBlur=excited?34:20;ctx.shadowColor=excited?'#c879ff':'#20cfff';
 const grad=ctx.createRadialGradient(x-8,y-10,3,x,y,40*pulse);
 grad.addColorStop(0,'#e9ffff');grad.addColorStop(.35,excited?'#d78cff':'#57eaff');grad.addColorStop(1,'#2369e8');
 ctx.fillStyle=grad;ctx.beginPath();ctx.arc(x,y,35*pulse,0,Math.PI*2);ctx.fill();ctx.restore();
 // Four surrounding atoms and bonds
 const pts=[[x-55,y-43],[x+55,y-43],[x-55,y+43],[x+55,y+43]];
 pts.forEach(p=>{line(x,y,p[0],p[1],excited?'#e5a1ff':'#5edfff',3);glowCircle(p[0],p[1],9,excited?'#d78cff':'#58dfff',14)});
 ctx.fillStyle='#f7fbff';ctx.font='bold 13px Arial';ctx.textAlign='center';ctx.fillText('MOLECULE',x,y+62);ctx.textAlign='left';
}
function draw(){
 ctx.clearRect(0,0,W,H);
 // subtle stars
 for(let i=0;i<32;i++){
  const x=(i*83+22)%W,y=(i*47+17)%H;
  ctx.fillStyle='rgba(110,170,255,.35)';ctx.beginPath();ctx.arc(x,y,1.5,0,Math.PI*2);ctx.fill();
 }
 const t=elapsed%duration;
 const cx=W*.52,cy=H*.53;
 let stage,excited=false;
 if(t<2){stage='Stage 1 · Excitation photon approaches the molecule';}
 else if(t<4){stage='Stage 2 · The molecule absorbs the photon';excited=true;}
 else if(t<6){stage='Stage 3 · Energy is lost by non-radiative relaxation';excited=true;}
 else {stage='Stage 4 · Fluorescence photon is emitted';}
 statusEl.textContent=(playing?'▶ ':'Ⅱ ')+stage;
 // energy-level guide
 ctx.setLineDash([5,6]);line(24,H-36,W-24,H-36,'rgba(150,190,240,.22)',1);ctx.setLineDash([]);
 ctx.fillStyle='#9fc8ff';ctx.font='12px Arial';ctx.fillText('Ground state (S₀)',20,H-15);
 ctx.fillStyle='#e6a5ff';ctx.fillText('Excited state (S₁)',W-132,H-15);
 drawMolecule(t,excited);
 if(t<2){
   const p=smooth(t/2);drawPhoton(28+p*(cx-65),cy,'#ffe45c','EXCITATION');
   line(25,cy,cx-65,cy,'rgba(255,228,92,.25)',2);
 }else if(t<4){
   const pulse=Math.sin((t-2)*Math.PI*3);
   for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(cx,cy,48+i*15+Math.abs(pulse)*5,0,Math.PI*2);ctx.strokeStyle='rgba(255,228,92,'+(0.45-i*.12)+')';ctx.lineWidth=2;ctx.stroke();}
   ctx.fillStyle='#ffe45c';ctx.font='bold 13px Arial';ctx.fillText('ABSORPTION',cx-42,35);
 }else if(t<6){
   // downward wavy relaxation arrow
   const p=(t-4)/2;
   ctx.beginPath();
   for(let i=0;i<=45;i++){let q=i/45;let x=cx+70+Math.sin(q*7*Math.PI)*5;let y=55+q*125;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
   ctx.strokeStyle='#fbbf65';ctx.lineWidth=3;ctx.stroke();
   ctx.fillStyle='#fbbf65';ctx.font='bold 12px Arial';ctx.fillText('ENERGY RELEASE',cx+82,105);
   ctx.beginPath();ctx.moveTo(cx+70,180);ctx.lineTo(cx+62,166);ctx.lineTo(cx+78,166);ctx.closePath();ctx.fill();
 }else{
   const p=smooth((t-6)/3);
   drawPhoton(cx+65+p*(W-cx-92),cy,'#55e8ff','EMISSION');
   line(cx+65,cy,W-25,cy,'rgba(85,232,255,.25)',2);
 }
}
function frame(ts){
 if(!last)last=ts;let dt=Math.min((ts-last)/1000,.05);last=ts;
 if(playing)elapsed+=dt;
 draw();requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
document.getElementById('play').onclick=()=>{playing=true;};
document.getElementById('pause').onclick=()=>{playing=false;};
document.getElementById('replay').onclick=()=>{elapsed=0;playing=true;};
</script>
</body>
</html>
"""
    components.html(html, height=505, scrolling=False)

tabs = st.tabs(["🏠 Home", "📘 Learn", "⚡ Simulator", "📈 Spectra", "🧪 Applications", "📝 Quiz"])

with tabs[0]:
    st.subheader("What is fluorescence?")
    st.write("Fluorescence is the emission of light by a substance after it absorbs light of a suitable wavelength.")
    fluorescence_animation()
    st.info("Watch the yellow excitation photon enter, the molecule absorb energy, and the cyan fluorescence photon leave.")

with tabs[1]:
    st.subheader("The four stages of fluorescence")
    st.markdown("""
    1. **Excitation:** A molecule absorbs an incoming photon and moves from the ground singlet state (S₀) to an excited singlet state (S₁).
    2. **Absorption:** The molecule gains energy from the photon.
    3. **Non-radiative relaxation:** Some energy is lost to the surroundings, often as molecular vibration/heat.
    4. **Fluorescence emission:** The molecule returns to a lower energy state and emits a photon. The emitted light usually has a longer wavelength.
    """)
    st.subheader("Stokes shift")
    st.latex(r"\text{Stokes shift}=\lambda_{emission}-\lambda_{excitation}")
    st.write("A positive Stokes shift means the emission wavelength is longer than the excitation wavelength.")

with tabs[2]:
    st.subheader("Change the wavelengths")
    c1, c2 = st.columns(2)
    with c1:
        excitation = st.slider("Excitation wavelength (nm)", 250, 500, 365, 5)
    with c2:
        shift = st.slider("Illustrative Stokes shift (nm)", 20, 150, 85, 5)
    emission = excitation + shift
    h = 6.62607015e-34
    c = 299792458
    e = 1.602176634e-19
    energy_exc = (h*c/(excitation*1e-9))/e
    energy_em = (h*c/(emission*1e-9))/e
    m1,m2,m3 = st.columns(3)
    with m1:
        st.metric("Excitation", f"{excitation} nm")
    with m2:
        st.metric("Emission", f"{emission} nm")
    with m3:
        st.metric("Stokes shift", f"{shift} nm")
    st.markdown("**Photon energy**")
    st.latex(r"E=\frac{hc}{\lambda}")
    a,b = st.columns(2)
    with a:
        st.metric("Excitation photon energy", f"{energy_exc:.3f} eV")
    with b:
        st.metric("Emission photon energy", f"{energy_em:.3f} eV")
    st.caption("These values are an illustrative teaching model, not a prediction for a real chemical sample.")

with tabs[3]:
    st.subheader("Illustrative fluorescence spectrum")
    excitation = st.slider("Excitation peak (nm)", 250, 500, 365, 5, key="spec_ex")
    emission = st.slider("Emission peak (nm)", excitation+20, min(excitation+150, 650), min(excitation+85,650), 5, key="spec_em")
    x = np.linspace(250, 700, 600)
    ex_curve = np.exp(-0.5*((x-excitation)/18)**2)
    em_curve = np.exp(-0.5*((x-emission)/25)**2)
    df = pd.DataFrame({"Excitation intensity": ex_curve, "Emission intensity": em_curve}, index=x)
    st.line_chart(df, height=350)
    st.write(f"**Illustrative Stokes shift:** {emission-excitation} nm")
    st.caption("X-axis: wavelength (nm). Y-axis: relative intensity (arbitrary units). Curves are illustrative Gaussian shapes, not experimental measurements.")

with tabs[4]:
    st.subheader("Where is fluorescence used?")
    items = [
        ("🩺 Medical imaging", "Fluorescent markers help researchers and clinicians observe cells and tissues."),
        ("🕵️ Forensic science", "Some materials and traces can fluoresce under suitable illumination."),
        ("🧬 Biotechnology", "Fluorescent labels help study DNA, proteins and cells."),
        ("🔬 Fluorescence microscopy", "Fluorescence makes selected structures easier to observe."),
        ("💧 Chemical analysis", "Fluorescence can help detect and estimate certain substances.")
    ]
    for title, desc in items:
        with st.expander(title):
            st.write(desc)

with tabs[5]:
    st.subheader("Test your understanding")
    questions = [
        ("What happens first in fluorescence?", ["Emission of light", "Absorption of a photon", "Molecule disappears"], 1,
         "The molecule first absorbs an incoming photon."),
        ("Fluorescence emission usually has:", ["Longer wavelength", "Shorter wavelength", "Exactly the same wavelength"], 0,
         "The emitted photon usually has lower energy and a longer wavelength."),
        ("What does Stokes shift compare?", ["Two intensities", "Emission and excitation wavelengths", "Two temperatures"], 1,
         "Stokes shift is emission wavelength minus excitation wavelength.")
    ]
    score = 0
    answers = []
    for i,(q,opts,correct,why) in enumerate(questions):
        ans = st.radio(q, opts, key=f"quiz_{i}")
        answers.append((ans,correct,why))
    if st.button("Check my answers"):
        for i,(ans,correct,why) in enumerate(answers):
            chosen = questions[i][1].index(ans)
            if chosen == correct:
                score += 1
                st.success(f"Q{i+1}: Correct! {why}")
            else:
                st.error(f"Q{i+1}: Not quite. {why}")
        st.metric("Your score", f"{score}/3")

st.divider()
st.caption("🔬 FluoroLab 2.0 | Engineering Chemistry | Unit II | Educational simulation")
    
