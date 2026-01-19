import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os
import time
import hashlib

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Cortex IA - Elite Portal (Eduzz Integrated)",
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

# --- CONEXÃO COM GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

def get_all_users():
    if conn:
        try:
            return conn.read(worksheet="Progresso", ttl="0s")
        except:
            return pd.DataFrame(columns=["email", "senha", "dia_atual", "notas"])
    return pd.DataFrame(columns=["email", "senha", "dia_atual", "notas"])

def save_user_data(df):
    if conn:
        try:
            conn.update(worksheet="Progresso", data=df)
        except Exception as e:
            st.error(f"Erro ao sincronizar: {e}")

# --- LÓGICA DE AUTENTICAÇÃO ---
if "user_email" not in st.session_state:
    st.session_state.user_email = None

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🧠 CORTEX IA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Área de Membros Eduzz</p>", unsafe_allow_html=True)
        
        email = st.text_input("E-mail da Compra", placeholder="seu@email.com").lower().strip()
        password = st.text_input("Senha", type="password", placeholder="Sua senha")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("ENTRAR"):
                df = get_all_users()
                user = df[df["email"] == email]
                
                if not user.empty:
                    # Verifica senha (aqui você pode usar hash para segurança real)
                    if str(user.iloc[0]["senha"]) == password:
                        st.session_state.user_email = email
                        st.session_state.dia_atual = int(user.iloc[0]["dia_atual"])
                        st.session_state.notas = str(user.iloc[0]["notas"])
                        st.success("Acesso autorizado!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Senha incorreta.")
                else:
                    st.error("E-mail não encontrado na lista de alunos Eduzz.")
        
        with col_btn2:
            st.markdown("<p style='font-size: 0.8rem; color: #555; text-align: center;'>Problemas no acesso?<br>Suporte: suporte@cortexia.com</p>", unsafe_allow_html=True)

# --- APP PRINCIPAL ---
if st.session_state.user_email is None:
    login_screen()
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"### Aluno:<br>**{st.session_state.user_email}**", unsafe_allow_html=True)
        st.markdown("---")
        dias = [f"Dia {i:02d}" for i in range(1, 22)]
        escolha_dia = st.selectbox("Módulo Atual", dias, index=min(st.session_state.dia_atual - 1, 20))
        dia_num = int(escolha_dia.split()[1])
        
        if st.button("LOGOUT"):
            st.session_state.user_email = None
            st.rerun()

    # Conteúdo
    st.title(f"🚀 {escolha_dia}")
    
    def load_content(day):
        base_path = os.path.dirname(__file__)
        content_dir = os.path.join(base_path, "content")
        if day == 1: filename = "curso_cortex_ia_dia_01_final_v3.md"
        elif day == 2: filename = "curso_cortex_ia_dia_02_final_v3.md"
        elif day == 21:
            parts = ["curso_cortex_ia_dia_21_intensivao_parte_1.md", "curso_cortex_ia_dia_21_intensivao_parte_2.md", "curso_cortex_ia_dia_21_intensivao_parte_3.md"]
            full = ""
            for p in parts:
                p_path = os.path.join(content_dir, p)
                if os.path.exists(p_path):
                    with open(p_path, "r", encoding="utf-8") as f: full += f.read() + "\n\n---\n\n"
            return full if full else "Erro: Intensivão não encontrado."
        else: filename = f"curso_cortex_ia_dia_{day:02d}_final.md"
        
        path = os.path.join(content_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: return f.read()
        return f"Erro: Conteúdo do Dia {day} não encontrado."

    content = load_content(dia_num)
    c_main, c_tools = st.columns([3, 1])
    
    with c_main:
        st.markdown(content)
        st.markdown("---")
        if st.button("CONCLUIR DIA"):
            df = get_all_users()
            new_day = dia_num + 1 if dia_num < 21 else 21
            df.loc[df["email"] == st.session_state.user_email, "dia_atual"] = new_day
            save_user_data(df)
            st.session_state.dia_atual = new_day
            st.balloons()
            st.success("Progresso salvo!")

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
        notas_input = st.text_area("Exercícios do dia:", value=st.session_state.get("notas", ""), height=300)
        if st.button("SALVAR NOTAS"):
            df = get_all_users()
            df.loc[df["email"] == st.session_state.user_email, "notas"] = notas_input
            save_user_data(df)
            st.session_state.notas = notas_input
            st.success("Notas salvas!")
