import streamlit as st
import streamlit.components.v1 as components
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Cortex IA - Elite Portal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- BARRA DE PROGRESSO POR SCROLL (TOPO) ---
components.html("""
<style>
#scroll-progress-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: rgba(0, 0, 0, 0.08);
    z-index: 999999;
}

#scroll-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #37D087, #39D7FE);
}
</style>

<div id="scroll-progress-container">
    <div id="scroll-progress-bar"></div>
</div>

<script>
(function () {
    const bar = document.getElementById("scroll-progress-bar");

    function updateProgress() {
        const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const percent = (scrollTop / scrollHeight) * 100;
        bar.style.width = percent + "%";
    }

    window.addEventListener("scroll", updateProgress);
})();
</script>
""", height=0)

# --- ESTILO PREMIUM (CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

html, body, .stApp {
    background-color: #F0FFFE !important;
}

/* Texto padrão */
.stMarkdown {
    color: #952791;
    line-height: 1.8;
}

/* Títulos */
h1, h2, h3 {
    color: #952791 !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

/* Botões */
.stButton > button {
    background: linear-gradient(90deg, #37D087 0%, #39D7FE 100%);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-weight: 700;
    border-radius: 8px;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(55, 208, 135, 0.4);
}
</style>
""", unsafe_allow_html=True)

# --- SISTEMA DE AUTENTICAÇÃO ---
CHAVE_MESTRA = "a"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>🧠 CORTEX IA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888;'>Portal de Elite - Acesso Rápido</p>", unsafe_allow_html=True)
        chave = st.text_input("Chave de Acesso", type="password")
        if st.button("LIBERAR ACESSO"):
            if chave == CHAVE_MESTRA:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Chave incorreta.")

# --- APP PRINCIPAL ---
if not st.session_state.authenticated:
    login_screen()
else:
    if "dia_atual" not in st.session_state:
        st.session_state.dia_atual = 1
    if "notas" not in st.session_state:
        st.session_state.notas = {}

    # Sidebar
    with st.sidebar:
        st.markdown("### 🧠 Cortex IA")
        st.markdown("---")
        dias = [f"Dia {i:02d}" for i in range(1, 22)]
        escolha_dia = st.selectbox(
            "Módulo Atual",
            dias,
            index=st.session_state.dia_atual - 1
        )
        dia_num = int(escolha_dia.split()[1])

        if st.button("SAIR"):
            st.session_state.authenticated = False
            st.rerun()

    # Conteúdo principal
    st.title(f"🚀 {escolha_dia}")

    def load_content(day):
        filename = f"curso_cortex_ia_dia_{day:02d}.md"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        return f"⚠️ Arquivo '{filename}' não encontrado."

    content = load_content(dia_num)

    c_main, c_tools = st.columns([3, 1])

    with c_main:
        st.markdown(content)
        st.markdown("---")
        if st.button("CONCLUIR DIA"):
            st.session_state.dia_atual = min(dia_num + 1, 21)
            st.balloons()
            st.success("Progresso marcado!")

    with c_tools:
        st.subheader("📝 Notas")
        notas_input = st.text_area(
            "Exercícios do dia:",
            value=st.session_state.notas.get(dia_num, ""),
            height=300
        )
        if st.button("SALVAR NOTAS"):
            st.session_state.notas[dia_num] = notas_input
            st.success("Notas salvas!")
