
import streamlit as st

st.set_page_config(
    page_title="FluoroLab",
    page_icon="🔬",
    layout="wide"
)

# Website design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07152e, #182c52, #321b50);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #173e70, #58317d);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #6ca9ff;
}
.hero h1 {
    font-size: 48px;
}
.hero p {
    font-size: 19px;
}
.card {
    background: #172c4b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #416b9c;
    min-height: 150px;
}
</style>
""", unsafe_allow_html=True)

# Main heading
st.markdown("""
<div class="hero">
    <h1>🔬 FluoroLab</h1>
    <h3>An Interactive Fluorescence Spectroscopy Simulator</h3>
    <p>Discover how molecules absorb and emit light!</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# Introduction
st.header("✨ Welcome to the World of Fluorescence")

st.write("""
Have you ever wondered why some materials glow when exposed
to ultraviolet light?

This phenomenon is called **Fluorescence**.

Fluorescence spectroscopy is a technique used to study
how substances absorb light and emit light at different
wavelengths.
""")

# Three learning cards
st.subheader("🧪 What will you learn?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>💡 Absorption</h3>
    <p>Understand how a molecule absorbs light energy.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>⚡ Excitation</h3>
    <p>Learn how a molecule moves to a higher energy state.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>🌈 Emission</h3>
    <p>Discover how a molecule releases light energy.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.info("This website is an educational simulation of fluorescence spectroscopy.")

st.markdown("---")
st.caption("FluoroLab | Engineering Chemistry | Unit II")
