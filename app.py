import streamlit as st
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cortex IA", page_icon="🧠", layout="wide")

# --- ESTILO PREMIUM (FOCO EM LEITURA) ---
st.markdown(\"\"\"
    <style>
    .main { background-color: #050505; }
    .stMarkdown { 
        color: #E0E0E0; 
        line-height: 1.8; 
        font-size: 1.1rem;
        max-width: 900px;
        margin: 0 auto;
    }
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 800 !important; }
    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF1F1F 100%);
        color: white; border-radius: 8px; width: 100%;
    }
    /* Garante que o container de texto não tenha limite de altura */
    .element-container { overflow: visible !important; }
    </style>
    \"\"\", unsafe_allow_html=True)

# --- LOGIN ---
if \"auth\" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title(\"🧠 CORTEX IA\")
    chave = st.text_input(\"Chave de Acesso\", type=\"password\")
    if st.button(\"ENTRAR\"):
        if chave == \"CORTEX-2026\":
            st.session_state.auth = True
            st.rerun()
        else: st.error(\"Chave incorreta.\")
    st.stop()

# --- NAVEGAÇÃO ---
dias = [f\"Dia {i:02d}\" for i in range(1, 22)]
escolha = st.sidebar.selectbox(\"Módulo Atual\", dias)
dia_num = int(escolha.split()[1])

# --- CARREGAMENTO DE CONTEÚDO ---
def load_content(day):
    base_path = os.path.dirname(__file__)
    
    # Tenta os dois padrões de nome (com e sem o zero à esquerda)
    filenames = [
        f\"curso_cortex_ia_dia_{day:02d}.md\",
        f\"curso_cortex_ia_dia_{day}.md\"
    ]
    
    # Caso especial para o Dia 21 (Intensivão)
    if day == 21:
        parts = [\"curso_cortex_ia_dia_21_intensivao_parte_1.md\", 
                 \"curso_cortex_ia_dia_21_intensivao_parte_2.md\", 
                 \"curso_cortex_ia_dia_21_intensivao_parte_3.md\"]
        full = \"\"
        for p in parts:
            p_path = os.path.join(base_path, p)
            if os.path.exists(p_path):
                with open(p_path, \"r\", encoding=\"utf-8\") as f: full += f.read() + \"\\n\\n---\\n\\n\"
        if full: return full

    for fname in filenames:
        path = os.path.join(base_path, fname)
        if os.path.exists(path):
            with open(path, \"r\", encoding=\"utf-8\") as f:
                return f.read()
                
    return f\"Erro: Arquivo não encontrado na raiz do GitHub. Verifique se o nome é {filenames[0]}\"

# --- EXIBIÇÃO ---
st.title(f\"🚀 {escolha}\")

# Layout em duas colunas apenas para ferramentas, texto ocupa o centro
col_txt, col_side = st.columns([3, 1])

with col_txt:
    conteudo_completo = load_content(dia_num)
    st.markdown(conteudo_completo, unsafe_allow_html=True)
    st.markdown(\"---")
    if st.button(\"CONCLUIR DIA\"): st.balloons()

with col_side:
    st.subheader(\"⏱️ Cronômetro\")
    if st.button(\"INICIAR 15 MIN\"):
        t = st.empty()
        for i in range(943, 0, -1):
            m, s = divmod(i, 60)
            t.metric(\"Restante\", f\"{m:02d}:{s:02d}\")
            time.sleep(1)
    
    st.markdown(\"---")
    st.subheader(\"📝 Notas\")
    st.text_area(\"Anote seus Brain-links:\", height=300)
    st.button(\"SALVAR NOTAS\")
