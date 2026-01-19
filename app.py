import streamlit as st

st.set_page_config(
    page_title="Cortex IA",
    layout="wide"
)

# ===== BARRA DE PROGRESSO POR SCROLL =====
st.markdown("""
<style>
/* Container da barra */
#scroll-progress-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background-color: rgba(255, 255, 255, 0.15);
    z-index: 9999;
}

/* Barra preenchida */
#scroll-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #ff2d2d, #ff6b6b);
    transition: width 0.05s linear;
}
</style>

<div id="scroll-progress-container">
    <div id="scroll-progress-bar"></div>
</div>

<script>
window.addEventListener("scroll", () => {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercent = (scrollTop / scrollHeight) * 100;
    document.getElementById("scroll-progress-bar").style.width = scrollPercent + "%";
});
</script>
""", unsafe_allow_html=True)

# ===== CONTEÚDO NORMAL DA PÁGINA =====
st.title("DIA 16: Os Estilos de Liderança e a Ressonância")

st.write("""
Role a página e observe a barra no topo sendo preenchida conforme a leitura.
""")

# Simula conteúdo longo (igual seu módulo)
for i in range(40):
    st.write(f"Conteúdo do módulo — parágrafo {i+1}")
