
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="FluoroLab 2.0",
    page_icon="🔬",
    layout="wide"
)

# -------------------- STYLING --------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#080d27,#17113d,#071e36);
    color: white;
}
h1,h2,h3 {
    color: #63eaff !important;
}
p,li,label {
    color: #e5eaff;
}
div[data-testid="stMetric"] {
    background: #18264b;
    border: 1px solid #3d8aff;
    padding: 15px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🔬 FluoroLab 2.0
### Colourful Interactive Fluorescence Spectroscopy Simulator

Explore light absorption, molecular excitation and fluorescence emission.

**Engineering Chemistry | Spectroscopic Techniques | Unit II**
""")

st.markdown("---")

# -------------------- ANIMATION ENGINE --------------------

animation_html = r"""
<!DOCTYPE html>
<html>
<head>
<style>
* {box-sizing:border-box}
body {
    margin:0;
    background:linear-gradient(120deg,#080d27,#171044,#071d38);
    font-family:Arial,sans-serif;
    color:white;
}
.panel {
    border:1px solid #345b99;
    border-radius:18px;
    padding:12px;
    background:rgba(10,20,55,.8);
}
canvas {
    width:100%;
    height:320px;
    display:block;
    touch-action:none;
    border-radius:12px;
}
.controls {
    display:flex;
    gap:9px;
    flex-wrap:wrap;
    margin-top:10px;
}
button {
    border:0;
    border-radius:10px;
    padding:10px 17px;
    color:white;
    background:linear-gradient(90deg,#087bdb,#8539d7);
    font-weight:bold;
    cursor:pointer;
}
button:hover {filter:brightness(1.3)}
#status {
    color:#65f4ff;
    margin-top:10px;
    font-size:14px;
}
small {color:#b9c9ed}
</style>
</head>
<body>

<div class="panel">
    <h3>✨ Live Fluorescence Animation</h3>
    <small>Drag the glowing molecule with your finger or mouse!</small>

    <canvas id="scene"></canvas>

    <div class="controls">
        <button onclick="play()">▶ Play</button>
        <button onclick="pause()">⏸ Pause</button>
        <button onclick="reset()">↻ Reset</button>
    </div>

    <div id="status">Ready: waiting for photon absorption</div>
</div>

<script>
const canvas = document.getElementById("scene");
const ctx = canvas.getContext("2d");
let W = 700, H = 320;
let running = true;
let t = 0;
let moleculeX = 350;
let moleculeY = 155;
let dragging = false;
let particles = [];

function resize() {
    let r = canvas.getBoundingClientRect();
    let dpr = window.devicePixelRatio || 1;
    canvas.width = r.width * dpr;
    canvas.height = r.height * dpr;
    W = r.width;
    H = r.height;
    ctx.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener("resize",resize);
resize();

function photon(x,y,color,r=6) {
    ctx.save();
    ctx.shadowBlur = 22;
    ctx.shadowColor = color;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x,y,r,0,Math.PI*2);
    ctx.fill();
    ctx.restore();
}

function label(txt,x,y,color,size=13) {
    ctx.fillStyle = color;
    ctx.font = "bold "+size+"px Arial";
    ctx.fillText(txt,x,y);
}

function drawMolecule() {
    let glow = 25 + 15*Math.sin(t*0.12);

    ctx.save();
    ctx.shadowBlur = glow;
    ctx.shadowColor = "#35eaff";

    let gradient = ctx.createRadialGradient(
        moleculeX-10,moleculeY-10,3,
        moleculeX,moleculeY,43
    );
    gradient.addColorStop(0,"#ffffff");
    gradient.addColorStop(.3,"#55eaff");
    gradient.addColorStop(.7,"#3876ff");
    gradient.addColorStop(1,"#8b38ff");

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(moleculeX,moleculeY,30+3*Math.sin(t*.1),0,Math.PI*2);
    ctx.fill();
    ctx.restore();

    let atoms = [
        [-42,-32],[42,-32],[-42,32],[42,32]
    ];

    atoms.forEach(([dx,dy])=>{
        ctx.strokeStyle="#a66bff";
        ctx.lineWidth=3;
        ctx.beginPath();
        ctx.moveTo(moleculeX,moleculeY);
        ctx.lineTo(moleculeX+dx,moleculeY+dy);
        ctx.stroke();
        photon(moleculeX+dx,moleculeY+dy,"#d78aff",7);
    });
}

function drawBackground() {
    for(let i=0;i<35;i++){
        let x=(i*97+Math.sin(t*.02+i)*15)%W;
        let y=(i*53+Math.cos(t*.02+i)*12)%H;
        photon(x,y,"rgba(95,155,255,.6)",1.5);
    }
}

function draw() {
    if(!running) return;

    ctx.clearRect(0,0,W,H);
    drawBackground();

    let cycle = t % 240;
    let incomingX = W*.08 + (W*.34)*(cycle/100);
    let outgoingX = moleculeX + 35 + (W*.42)*(Math.max(0,cycle-120)/100);

    if(cycle < 100) {
        photon(incomingX,H*.49,"#ffe65c",8);
        label("EXCITATION PHOTON",12,35,"#ffe65c");
        document.getElementById("status").textContent =
            "Stage 1: Molecule absorbs incoming light energy";
    } else if(cycle < 120) {
        label("EXCITED STATE",W*.39,35,"#ff80dc");
        document.getElementById("status").textContent =
            "Stage 2: Molecule reaches an excited state";
    } else if(cycle < 220) {
        photon(outgoingX,H*.49,"#38ffd0",8);
        label("EMISSION PHOTON",W*.72,35,"#38ffd0");
        document.getElementById("status").textContent =
            "Stage 3: Molecule emits fluorescence light";
    } else {
        document.getElementById("status").textContent =
            "Cycle complete: fluorescence demonstrated";
    }

    drawMolecule();

    label("S0: Ground state",12,H-22,"#8ecfff");
    label("S1: Excited state",W*.72,H-22,"#ff9de5");

    if(!dragging) t++;
    requestAnimationFrame(draw);
}

function play() {
    if(!running) {
        running = true;
        requestAnimationFrame(draw);
    }
}

function pause() {
    running = false;
}

function reset() {
    t = 0;
    moleculeX = W/2;
    moleculeY = H/2;
    if(!running) play();
}

function pointerPosition(e) {
    let r=canvas.getBoundingClientRect();
    return {
        x:e.clientX-r.left,
        y:e.clientY-r.top
    };
}

canvas.addEventListener("pointerdown",e=>{
    let p=pointerPosition(e);
    if(Math.hypot(p.x-moleculeX,p.y-moleculeY)<65) {
        dragging=true;
        canvas.setPointerCapture(e.pointerId);
    }
});

canvas.addEventListener("pointermove",e=>{
    if(dragging) {
        let p=pointerPosition(e);
        moleculeX=Math.max(55,Math.min(W-55,p.x));
        moleculeY=Math.max(65,Math.min(H-65,p.y));
    }
});

canvas.addEventListener("pointerup",()=>dragging=false);
canvas.addEventListener("pointercancel",()=>dragging=false);

requestAnimationFrame(draw);
</script>
</body>
</html>
"""

# -------------------- TABS --------------------

home, learn, simulator, spectra, applications, quiz = st.tabs([
    "🏠 Home",
    "📚 Learn",
    "⚡ Simulator",
    "📈 Spectra",
    "🧪 Applications",
    "🎯 Quiz"
])

# -------------------- HOME --------------------

with home:
    st.header("Welcome to FluoroLab!")

    st.markdown("""
    Fluorescence spectroscopy studies the light emitted by a
    substance after it absorbs light energy.

    This interactive project combines Chemistry and Python
    to make learning easier and more interesting.
    """)

    st.subheader("Watch the molecule in motion")
    components.html(animation_html,height=405,scrolling=False)

    c1,c2,c3 = st.columns(3)
    c1.info("💡 Light absorption")
    c2.info("⚛️ Molecular excitation")
    c3.info("✨ Fluorescence emission")

# -------------------- LEARN --------------------

with learn:
    st.header("Understanding fluorescence")

    st.subheader("How does fluorescence work?")

    st.markdown("""
    **1. Absorption:** A molecule absorbs a photon and moves
    from its ground singlet state S0 to an excited singlet state S1.

    **2. Relaxation:** The molecule loses some energy through
    non-radiative processes.

    **3. Emission:** The molecule releases a photon and returns
    to a lower energy state.
    """)

    st.subheader("Animated molecular process")
    components.html(animation_html,height=405,scrolling=False)

    st.subheader("Stokes shift")

    st.write("""
    Stokes shift is the difference between emission wavelength
    and excitation wavelength.
    """)

    st.latex(
        r"\text{Stokes shift} = "
        r"\lambda_{\text{emission}} - "
        r"\lambda_{\text{excitation}}"
    )

    st.success("Example: 450 nm - 365 nm = 85 nm")

# -------------------- SIMULATOR --------------------

with simulator:
    st.header("Interactive wavelength simulator")

    excitation = st.slider(
        "Choose excitation wavelength (nm)",
        min_value=300,
        max_value=450,
        value=365,
        step=5
    )

    # Illustrative fixed difference
    emission = excitation + 85
    stokes = emission - excitation

    h = 6.62607015e-34
    c = 299792458
    e = 1.602176634e-19

    energy_exc = (h*c/(excitation*1e-9))/e
    energy_em = (h*c/(emission*1e-9))/e

    a,b,d = st.columns(3)
    a.metric("Excitation",f"{excitation} nm")
    b.metric("Emission",f"{emission} nm")
    d.metric("Stokes shift",f"{stokes} nm")

    x,y = st.columns(2)
    x.metric("Excitation energy",f"{energy_exc:.3f} eV")
    y.metric("Emission energy",f"{energy_em:.3f} eV")

    st.subheader("Live moving molecule")
    components.html(animation_html,height=405,scrolling=False)

    st.warning("""
    Educational simulation: emission is set to excitation + 85 nm
    for demonstration. These values are illustrative and are not
    real experimental measurements or molecular predictions.
    """)

# -------------------- SPECTRA --------------------

with spectra:
    st.header("Colourful excitation and emission spectra")

    wavelengths = np.linspace(250,700,451)

    excitation_intensity = np.exp(
        -0.5*((wavelengths-365)/22)**2
    )

    emission_intensity = np.exp(
        -0.5*((wavelengths-450)/30)**2
    )

    df = pd.DataFrame({
        "Wavelength (nm)":wavelengths,
        "Excitation spectrum":excitation_intensity,
        "Emission spectrum":emission_intensity
    })

    st.write("""
    The following graph contains two illustrative Gaussian peaks.
    """)

    st.line_chart(
        df,
        x="Wavelength (nm)",
        y=["Excitation spectrum","Emission spectrum"],
        color=["#27C9FF","#FF4BCB"]
    )

    st.subheader("How to read the graph")

    st.markdown("""
    - **X-axis:** Wavelength in nanometres.
    - **Y-axis:** Relative intensity.
    - **Excitation peak:** Around 365 nm.
    - **Emission peak:** Around 450 nm.
    """)

    st.info("""
    These are simulated spectra for educational purposes,
    not experimental measurements.
    """)

# -------------------- APPLICATIONS --------------------

with applications:
    st.header("Applications of fluorescence spectroscopy")

    applications_list = [
        ("🏥 Medical research",
         "Used in biological imaging and studying cells."),
        ("🔍 Forensic science",
         "Helps examine fluorescent materials and evidence."),
        ("🧬 Biotechnology",
         "Used to study proteins and biomolecules."),
        ("🧪 Chemical analysis",
         "Helps detect and analyse fluorescent substances."),
        ("🔬 Fluorescence microscopy",
         "Helps observe structures in biological samples.")
    ]

    for title,description in applications_list:
        st.markdown(f"### {title}")
        st.write(description)
        st.markdown("---")

# -------------------- QUIZ --------------------

with quiz:
    st.header("Test your knowledge")

    questions = [
        {
            "q":"What is fluorescence?",
            "options":[
                "Emission of light after absorption",
                "Reflection of sound",
                "Heating of a molecule"
            ],
            "answer":"Emission of light after absorption"
        },
        {
            "q":"What does S0 represent?",
            "options":[
                "Excited state",
                "Ground singlet state",
                "Emission wavelength"
            ],
            "answer":"Ground singlet state"
        },
        {
            "q":"What is the Stokes shift in our example?",
            "options":["50 nm","85 nm","100 nm"],
            "answer":"85 nm"
        },
        {
            "q":"Which library generates numerical data?",
            "options":["NumPy","Streamlit","HTML"],
            "answer":"NumPy"
        },
        {
            "q":"What is the horizontal axis of the spectra graph?",
            "options":["Time","Temperature","Wavelength"],
            "answer":"Wavelength"
        }
    ]

    with st.form("fluorolab_quiz"):
        answers = []

        for i,question in enumerate(questions):
            st.write(f"**{i+1}. {question['q']}**")

            selected = st.radio(
                "Select your answer:",
                question["options"],
                key=f"question_{i}"
            )

            answers.append(selected)

        submitted = st.form_submit_button("Check my score")

    if submitted:
        score = sum(
            answers[i] == questions[i]["answer"]
            for i in range(len(questions))
        )

        st.success(f"Your score: {score}/5")

        for i,question in enumerate(questions):
            if answers[i] == question["answer"]:
                st.write(f"✅ Question {i+1}: Correct")
            else:
                st.write(
                    f"❌ Question {i+1}: "
                    f"Correct answer: {question['answer']}"
                )

        if score == 5:
            st.balloons()

# -------------------- FOOTER --------------------

st.markdown("---")
st.markdown(
    "<center>🔬 FluoroLab 2.0 | Engineering Chemistry | Unit II</center>",
    unsafe_allow_html=True
    )
    
