import streamlit as st
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Inteligência Cortex",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ESTILO PREMIUM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    html, body, .stApp {
    background-color: #F0FFFE !important;
}
#Cor da fonte menor
    .stMarkdown { color: #952791; line-height: 1.8; }
    h1, h2, h3 { color: #952791 !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    .stButton>button {
        background: linear-gradient(90deg, #37D087 0%, #39D7FE 100%);
        color: white; border: none; padding: 0.75rem 1.5rem;
        font-weight: 700; border-radius: 8px; transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 0.05em; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4); }
    .timer-card { background: #111111; border: 1px solid #222222; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
    .timer-value { font-size: 2rem; font-weight: 800; color: #FF4B4B; }
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
        st.markdown("<h1 style='text-align: center;'>🧠 Inteligência Cortex</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Portal de aprendizado</p>", unsafe_allow_html=True)
        chave = st.text_input("Chave de Acesso", type="password", placeholder="Digite sua chave")
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
    if 'dia_atual' not in st.session_state: st.session_state.dia_atual = 1
    if 'notas' not in st.session_state: st.session_state.notas = {}

    # Sidebar
    with st.sidebar:
        st.markdown("### 🧠 Inteligência Cortex")
        st.markdown("---")
        dias = [f"Dia {i:02d}" for i in range(1, 23)]
        escolha_dia = st.selectbox("Módulo Atual", dias, index=st.session_state.dia_atual - 1)
        dia_num = int(escolha_dia.split()[1])
        if st.button("SAIR"):
            st.session_state.authenticated = False
            st.rerun()

    # Conteúdo
    st.title(f"🚀 {escolha_dia}")
    
    def load_content(day):
        # Tenta encontrar o arquivo na raiz do repositório
        filename = f"curso_cortex_ia_dia_{day:02d}.md"
        
        # No Streamlit Cloud, os arquivos ficam na raiz do diretório de execução
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        
        # Fallback: tenta caminhos alternativos que o Streamlit pode usar
        alt_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(alt_path):
            with open(alt_path, "r", encoding="utf-8") as f:
                return f.read()
                
        return f"Erro: O arquivo '{filename}' não foi encontrado na raiz do seu GitHub. Verifique se o nome está exatamente assim."

    content = load_content(dia_num)
    c_main, c_tools = st.columns([3, 1])
    
    with c_main:
        st.markdown(content)
        st.markdown("---")
        if st.button("CONCLUIR DIA"):
            st.session_state.dia_atual = dia_num + 1 if dia_num < 22 else 22
            st.balloons()
            st.success("Progresso marcado!")

    with c_tools:
        st.markdown(f'<div class="timer-card"><p style="color:#888">FOCO</p><div class="timer-value">{"60:00" if dia_num==21 else "15:43"}</div></div>', unsafe_allow_html=True)
        if st.button("START TIMER"):
            p = st.empty()
            s = 3600 if dia_num==21 else 943
            while s > 0:
                m, sec = divmod(s, 60)
                p.markdown(f'<div class="timer-card"><p style="color:#888">RESTANTE</p><div class="timer-value">{m:02d}:{sec:02d}</div></div>', unsafe_allow_html=True)
                time.sleep(1); s -= 1
        
        st.markdown("---")
        st.subheader("📝 Notas")
        notas_input = st.text_area("Exercícios do dia:", value=st.session_state.notas.get(dia_num, ""), height=300)
        if st.button("SALVAR NOTAS"):
            st.session_state.notas[dia_num] = notas_input
            st.success("Notas salvas!")
