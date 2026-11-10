
import streamlit as st
import numpy as np
import pandas as pd

# ---------------------------------
# 1. PAGE SETTINGS
# ---------------------------------
st.set_page_config(
    page_title="FluoroLab",
    page_icon="🔬",
    layout="wide"
)

# ---------------------------------
# 2. WEBSITE DESIGN
# ---------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07152e, #142b50, #301b50);
    color: white;
}
h1, h2, h3, h4, p, label {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #123c70, #653b88);
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid #7bc8ff;
}
.hero h1 {
    font-size: 48px;
}
.hero p {
    font-size: 19px;
}
.card {
    background: #172d4d;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #4775a8;
    min-height: 145px;
}
.small-note {
    background: #173a4c;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# 3. HEADER
# ---------------------------------
st.markdown("""
<div class="hero">
    <h1>🔬 FluoroLab</h1>
    <h3>Interactive Fluorescence Spectroscopy Simulator</h3>
    <p>Explore how molecules absorb and emit light!</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.caption("ENGINEERING CHEMISTRY | UNIT II | EDUCATIONAL SIMULATION")

# ---------------------------------
# 4. NAVIGATION
# ---------------------------------
home, learn, simulator, spectra, applications, quiz = st.tabs([
    "🏠 Home",
    "📘 Learn",
    "⚡ Simulator",
    "📈 Spectra",
    "🧪 Applications",
    "📝 Quiz"
])

# ---------------------------------
# 5. HOME
# ---------------------------------
with home:
    st.header("✨ Welcome to FluoroLab!")

    st.write("""
    Have you ever wondered why some substances glow
    when exposed to ultraviolet light?

    This phenomenon is called **fluorescence**.

    Fluorescence spectroscopy is a technique that studies
    the light emitted by a substance after it absorbs light.
    """)

    st.subheader("What will you learn?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h3>💡 Absorption</h3>
        <p>A molecule absorbs light energy.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <h3>⚡ Excitation</h3>
        <p>The molecule reaches a higher electronic energy state.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        <h3>🌈 Emission</h3>
        <p>The molecule releases light and returns to a lower energy state.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.info(
        "Explore the tabs above to learn the theory, "
        "try the simulator and test your knowledge."
    )

# ---------------------------------
# 6. LEARN
# ---------------------------------
with learn:
    st.header("📘 Understanding Fluorescence")

    st.subheader("What is fluorescence?")

    st.write("""
    Fluorescence is the emission of light by a substance
    after it absorbs light energy.

    It usually happens very quickly after absorption.
    """)

    st.subheader("The four important steps")

    st.markdown("""
    **1. Absorption:** The molecule absorbs incoming light.

    **2. Excitation:** An electron moves to a higher
    electronic energy state.

    **3. Relaxation:** The molecule loses some energy
    without emitting light.

    **4. Fluorescence emission:** The molecule releases
    light and returns to a lower electronic energy state.
    """)

    st.subheader("Energy-level diagram (Jablonski model)")

    st.markdown("""
    <div style="background:#172d4d;padding:20px;border-radius:15px;">
    <h3 style="color:#8edcff;text-align:center;">Jablonski Diagram</h3>
    <div style="display:flex;justify-content:space-around;align-items:center;flex-wrap:wrap;gap:12px;">
      <div style="text-align:center;">
        <div style="color:#ffdf70;font-size:18px;">↑ Absorption</div>
        <div style="border-top:5px solid #ffdf70;width:100px;margin:15px auto;"></div>
        <div style="color:white;">S₁ excited state</div>
        <div style="color:#65e4c2;font-size:18px;margin:12px;">↓ Relaxation</div>
        <div style="border-top:5px solid #65e4c2;width:100px;margin:15px auto;"></div>
        <div style="color:white;">S₀ ground state</div>
      </div>
      <div style="text-align:center;color:#ff8de1;font-size:19px;">
        Fluorescence emission<br>↓
      </div>
    </div>
    <p style="color:#dcecff;text-align:center;">
    Simplified energy-level illustration. S₀ = ground singlet state;
    S₁ = first excited singlet state.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.info("""
    Remember: The molecule absorbs energy, loses some energy
    during relaxation, and then emits light.
    """)

    st.subheader("What is Stokes shift?")

    st.write("""
    Stokes shift is the difference between the emission
    wavelength and excitation wavelength in this simplified
    fluorescence example.
    """)

    st.latex(r"\text{Stokes shift}=\lambda_{emission}-\lambda_{excitation}")

    st.write("""
    The emission wavelength is usually longer because
    some absorbed energy is lost before fluorescence emission.
    """)

# ---------------------------------
# 7. SIMULATOR
# ---------------------------------
with simulator:
    st.header("⚡ Interactive Fluorescence Simulator")

    st.write("""
    Change the excitation wavelength and observe an
    illustrative emission wavelength.
    """)

    excitation = st.slider(
        "Choose excitation wavelength (nm)",
        min_value=300,
        max_value=450,
        value=365,
        step=5
    )

    # Simplified educational model
    emission = excitation + 85
    stokes_shift = emission - excitation

    st.subheader("Your simulation results")

    a, b, c = st.columns(3)

    with a:
        st.metric("Excitation", f"{excitation} nm")

    with b:
        st.metric("Emission", f"{emission} nm")

    with c:
        st.metric("Stokes shift", f"{stokes_shift} nm")

    st.write("### What does this mean?")

    st.success(
        f"The molecule absorbs light at {excitation} nm "
        f"and, in this illustrative model, emits light at "
        f"{emission} nm."
    )

    st.latex(
        r"\text{Stokes shift}="
        + str(emission)
        + "-"
        + str(excitation)
        + "="
        + str(stokes_shift)
        + r"\text{ nm}"
    )

    st.caption(
        "Educational model: emission is set 85 nm above "
        "excitation for demonstration. These are not "
        "experimental measurements or predictions for a real substance."
    )

    st.subheader("Photon energy")

    h = 6.62607015e-34
    c_light = 299792458
    e = 1.602176634e-19

    energy_ex = (
        h * c_light / (excitation * 1e-9)
    ) / e

    energy_em = (
        h * c_light / (emission * 1e-9)
    ) / e

    x, y = st.columns(2)

    with x:
        st.metric("Excitation photon energy", f"{energy_ex:.3f} eV")

    with y:
        st.metric("Emission photon energy", f"{energy_em:.3f} eV")

    st.write(
        "The emitted photon has lower energy because "
        "the molecule loses some energy before emission."
    )

# ---------------------------------
# 8. SPECTRA
# ---------------------------------
with spectra:
    st.header("📈 Understanding the Spectra")

    st.write("""
    A spectrum shows how light intensity varies with wavelength.
    The following graph is a simulated illustration with
    two separate peaks.
    """)

    wavelengths = np.linspace(250, 700, 500)

    excitation_peak = 365
    emission_peak = 450

    excitation_curve = np.exp(
        -0.5 * ((wavelengths - excitation_peak) / 18) ** 2
    )

    emission_curve = np.exp(
        -0.5 * ((wavelengths - emission_peak) / 25) ** 2
    )

    graph = pd.DataFrame({
        "Excitation (illustrative)": excitation_curve,
        "Emission (illustrative)": emission_curve
    }, index=wavelengths)

    st.line_chart(graph)

    st.info("""
    The first peak represents excitation light.
    The second peak represents emitted fluorescence.
    The emission peak appears at a longer wavelength.
    """)

    st.caption(
        "Illustrative Gaussian curves, not experimental spectral data."
    )

# ---------------------------------
# 9. APPLICATIONS
# ---------------------------------
with applications:
    st.header("🧪 Applications of Fluorescence")

    st.subheader("1. Medical research")
    st.write(
        "Fluorescent markers help researchers observe "
        "cells and biological processes."
    )

    st.subheader("2. Forensic science")
    st.write(
        "Fluorescence can help reveal certain materials "
        "and traces during forensic examination."
    )

    st.subheader("3. Biotechnology")
    st.write(
        "Fluorescent labels are used to study proteins, "
        "DNA and other biological molecules."
    )

    st.subheader("4. Chemical analysis")
    st.write(
        "Fluorescence measurements can help detect "
        "and study certain chemical substances."
    )

    st.subheader("5. Fluorescence microscopy")
    st.write(
        "Scientists use fluorescent dyes to make "
        "specific structures visible under a microscope."
    )

# ---------------------------------
# 10. QUIZ
# ---------------------------------
with quiz:
    st.header("📝 Test Your Knowledge")

    questions = [
        {
            "q": "1. What is fluorescence?",
            "options": [
                "Absorption of sound",
                "Emission of light after absorption",
                "Reflection of sound",
                "Production of heat only"
            ],
            "answer": "Emission of light after absorption",
            "why": "A fluorescent substance emits light after absorbing light energy."
        },
        {
            "q": "2. What happens during excitation?",
            "options": [
                "Electron moves to a higher energy state",
                "Molecule disappears",
                "Light becomes sound",
                "Temperature becomes zero"
            ],
            "answer": "Electron moves to a higher energy state",
            "why": "Absorbed energy can promote an electron to a higher electronic state."
        },
        {
            "q": "3. What is the usual relation between emission and excitation wavelength?",
            "options": [
                "Emission is shorter",
                "Both are always equal",
                "Emission is longer",
                "There is no light"
            ],
            "answer": "Emission is longer",
            "why": "Some energy is lost before fluorescence emission."
        },
        {
            "q": "4. Which diagram represents electronic energy states?",
            "options": [
                "Circuit diagram",
                "Jablonski diagram",
                "Bar chart",
                "Flowchart"
            ],
            "answer": "Jablonski diagram",
            "why": "A Jablonski diagram illustrates electronic states and transitions."
        },
        {
            "q": "5. Fluorescence is useful in which field?",
            "options": [
                "Medical research",
                "Biotechnology",
                "Chemical analysis",
                "All of these"
            ],
            "answer": "All of these",
            "why": "Fluorescence has applications in all these fields."
        }
    ]

    answers = []

    for i, question in enumerate(questions):
        st.write("")
        st.subheader(question["q"])

        selected = st.radio(
            "Choose your answer:",
            question["options"],
            key=f"question_{i}"
        )

        answers.append(selected)

    if st.button("Submit Quiz"):
        score = 0

        for i, question in enumerate(questions):
            if answers[i] == question["answer"]:
                score += 1

        st.success(f"Your score: {score} / {len(questions)}")

        for i, question in enumerate(questions):
            if answers[i] == question["answer"]:
                st.write(f"✅ Question {i+1}: Correct!")
            else:
                st.write(
                    f"❌ Question {i+1}: Correct answer: "
                    f"{question['answer']}"
                )

            st.caption(question["why"])

        if score == 5:
            st.balloons()
            st.write("Excellent! You are a FluoroLab expert!")

        elif score >= 3:
            st.write("Good work! Keep learning.")

        else:
            st.write("Review the Learn section and try again.")

# ---------------------------------
# 11. FOOTER
# ---------------------------------
st.markdown("---")

st.markdown(
    "<p style='text-align:center;color:#b8d7ff;'>"
    "🔬 FluoroLab | Engineering Chemistry | Unit II"
    "</p>",
    unsafe_allow_html=True
)

