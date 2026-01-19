import streamlit as st
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Cortex IA - Elite Portal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

/* Texto menor */
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

/* Card do Timer */
.timer-card {
    background: #111111;
    border: 1px solid #222222;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 15px;
}

.timer-value {
    font-size: 2rem;
    font-weight: 800;
    color: #FF4B4B;
}

/* Barra de progresso custom */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #37D087, #39D7FE);
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

    # --- TIMER + PROGRESSO ---
    with c_tools:
        duracao = 3600 if dia_num == 21 else 943

        timer_box = st.empty()
        progress_bar = st.empty()

        timer_box.markdown(
            f"""
            <div class="timer-card">
                <p style="color:#888">FOCO</p>
                <div class="timer-value">
                    {duracao // 60:02d}:{duracao % 60:02d}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("START TIMER"):
            progresso = progress_bar.progress(0.0)

            for i in range(duracao):
                restante = duracao - i
                m, s = divmod(restante, 60)

                timer_box.markdown(
                    f"""
                    <div class="timer-card">
                        <p style="color:#888">RESTANTE</p>
                        <div class="timer-value">{m:02d}:{s:02d}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                progresso.progress((i + 1) / duracao)
                time.sleep(1)

        st.markdown("---")
        st.subheader("📝 Notas")
        notas_input = st.text_area(
            "Exercícios do dia:",
            value=st.session_state.notas.get(dia_num, ""),
            height=300
        )
        if st.button("SALVAR NOTAS"):
            st.session_state.notas[dia_num] = notas_input
            st.success("Notas salvas!")
