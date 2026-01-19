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
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #050505; }
    .stMarkdown { color: #E0E0E0; line-height: 1.8; }
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF1F1F 100%);
        color: white; border: none; padding: 0.75rem 1.5rem;
        font-weight: 700; border-radius: 8px; transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 0.05em; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4); }
    .timer-card { background: #111111; border: 1px solid #222222; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
    .timer-value { font-size: 2rem; font-weight: 800; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE AUTENTICAÇÃO SIMPLIFICADO ---
CHAVE_MESTRA = "CORTEX-2026"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🧠 CORTEX IA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Portal de Elite - Acesso Rápido</p>", unsafe_allow_html=True)
        
        chave = st.text_input("Chave de Acesso", type="password", placeholder="Digite sua chave para testar")
        
        if st.button("LIBERAR ACESSO"):
            if chave == CHAVE_MESTRA:
                st.session_state.authenticated = True
                st.success("Acesso autorizado! Carregando...")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Chave incorreta. Tente 'CORTEX-2026'")

# --- APP PRINCIPAL ---
if not st.session_state.authenticated:
    login_screen()
else:
    # Inicialização de variáveis de sessão
    if 'dia_atual' not in st.session_state:
        st.session_state.dia_atual = 1
    if 'notas' not in st.session_state:
        st.session_state.notas = {}

    # Sidebar
    with st.sidebar:
        st.markdown("### 🧠 Cortex IA", unsafe_allow_html=True)
        st.markdown("---")
        dias = [f"Dia {i:02d}" for i in range(1, 22)]
        escolha_dia = st.selectbox("Módulo Atual", dias, index=st.session_state.dia_atual - 1)
        dia_num = int(escolha_dia.split()[1])
        
        if st.button("SAIR"):
            st.session_state.authenticated = False
            st.rerun()

    # Conteúdo
    st.title(f"🚀 {escolha_dia}")
    
    def load_content(day):
        base_path = os.path.dirname(__file__)
        content_dir = os.path.join(base_path, "content")
        
        # Mapeamento exato dos arquivos
        if day == 1: filename = "curso_cortex_ia_dia_01_final_v3.md"
        elif day == 2: filename = "curso_cortex_ia_dia_02_final_v3.md"
        elif day == 21:
            parts = ["curso_cortex_ia_dia_21_intensivao_parte_1.md", 
                     "curso_cortex_ia_dia_21_intensivao_parte_2.md", 
                     "curso_cortex_ia_dia_21_intensivao_parte_3.md"]
            full = ""
            for p in parts:
                p_path = os.path.join(content_dir, p)
                if os.path.exists(p_path):
                    with open(p_path, "r", encoding="utf-8") as f: full += f.read() + "\n\n---\n\n"
            return full if full else "Erro: Intensivão não encontrado."
        else:
            filename = f"curso_cortex_ia_dia_{day:02d}_final.md"
        
        path = os.path.join(content_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: return f.read()
        return f"Erro: Conteúdo do Dia {day} não encontrado no caminho: {path}"

    content = load_content(dia_num)
    c_main, c_tools = st.columns([3, 1])
    
    with c_main:
        st.markdown(content)
        st.markdown("---")
        if st.button("CONCLUIR DIA"):
            st.session_state.dia_atual = dia_num + 1 if dia_num < 21 else 21
            st.balloons()
            st.success("Progresso marcado! (Nesta versão de teste, o progresso reseta ao fechar o navegador)")

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
            st.success("Notas salvas temporariamente!")
