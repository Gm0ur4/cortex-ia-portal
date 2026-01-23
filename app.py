import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Inteligência Cortex - Aula Gratuita",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ESTILO PREMIUM (CSS) ---
# Mantivemos seu estilo original para consistência visual
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    html, body, .stApp {
        background-color: #F0FFFE !important;
    }
    .stMarkdown { color: #952791; line-height: 1.8; }
    h1, h2, h3 { color: #952791 !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    .stButton>button {
        background: linear-gradient(90deg, #37D087 0%, #39D7FE 100%);
        color: white; border: none; padding: 0.75rem 1.5rem;
        font-weight: 700; border-radius: 8px; transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 0.05em; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4); }
    
    /* Adicionei um estilo extra para esconder o menu padrão do Streamlit se desejar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DEFINIÇÃO DO DIA FIXO ---
DIA_FIXO = 13  # Define que esta página só carrega o dia 13

# --- FUNÇÃO DE CARREGAMENTO (Igual ao original) ---
def load_content(day):
    filename = f"curso_cortex_ia_dia_{day:02d}.md"
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    
    # Fallback
    alt_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(alt_path):
        with open(alt_path, "r", encoding="utf-8") as f:
            return f.read()
            
    return f"⚠️ Erro: O arquivo '{filename}' não foi encontrado. Certifique-se de que ele está no repositório GitHub desta nova URL."

# --- SIDEBAR (Simplificada para Marketing) ---
with st.sidebar:
    st.markdown("### 🧠 Inteligência Cortex")
    st.markdown("---")
    st.info("Esta é uma aula demonstrativa do nosso curso completo.")
    
    # Aqui você pode colocar o link para comprar o curso completo
    st.link_button("🔓 GARANTIR ACESSO TOTAL", "https://seu-link-de-compra.com")
    
# --- CONTEÚDO PRINCIPAL ---
st.title(f"🚀 Dia {DIA_FIXO:02d} (Demonstração)")

content = load_content(DIA_FIXO)
c_main, c_tools = st.columns([3, 1])

with c_main:
    st.markdown(content)
    st.markdown("---")
    
    # Call to Action no final da leitura
    st.success("Gostou do conteúdo? Tenha acesso aos outros 21 dias agora mesmo.")
    if st.button("QUERO APRENDER TUDO"):
        st.markdown("[Clique aqui para se inscrever](https://seu-link-de-compra.com)")
        st.balloons()

with c_tools:
    st.markdown("---")
    st.subheader("📝 Teste o Bloco de Notas")
    st.caption("No curso completo, suas anotações ficam salvas.")
    notas_input = st.text_area("Exercícios do dia:", placeholder="Escreva suas ideias aqui...", height=300)
    
    if st.button("SALVAR (DEMO)"):
        st.toast("Nota registrada temporariamente!", icon="✅")
