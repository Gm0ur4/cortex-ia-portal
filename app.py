import streamlit as st
import os
import time

# Configuração da Página
st.set_page_config(
    page_title="Cortex IA - Portal do Mestre",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SISTEMA DE SEGURANÇA (CHAVES DE ACESSO) ---
# Você pode adicionar ou remover chaves nesta lista
CHAVES_VALIDAS = ["CORTEX-2026-MASTER", "ALUNO-VIP-01", "ACESSO-LIBERADO"]

def check_password():
    """Retorna True se o usuário inseriu uma chave válida."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    # Tela de Login
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/564/564445.png", width=100)
        st.title("Acesso Restrito - Cortex IA")
        st.write("Digite sua chave de acesso individual para liberar o conteúdo.")
        
        password = st.text_input("Chave de Acesso", type="password")
        if st.button("Liberar Portal"):
            if password in CHAVES_VALIDAS:
                st.session_state.authenticated = True
                st.success("Acesso Liberado! Carregando...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Chave inválida. Sacou? Tente novamente ou entre em contato com o suporte.")
    return False

# Estilo Customizado (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMarkdown {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .timer-box {
        padding: 10px;
        border-radius: 10px;
        background-color: #262730;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Só executa o app se estiver autenticado
if check_password():
    # Inicialização do Estado (Progresso)
    if 'dia_atual' not in st.session_state:
        st.session_state.dia_atual = 1
    if 'exercicios' not in st.session_state:
        st.session_state.exercicios = {}

    # Sidebar - Navegação
    st.sidebar.title("🧠 Cortex IA")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Seu Progresso")

    dias = [f"Dia {i:02d}" for i in range(1, 22)]
    escolha_dia = st.sidebar.selectbox("Selecione o Dia", dias, index=st.session_state.dia_atual - 1)
    dia_num = int(escolha_dia.split()[1])

    st.sidebar.markdown("---")
    st.sidebar.info("Mantenha o foco. O aprendizado real exige tempo no Modo Focado.")
    
    if st.sidebar.button("Sair / Bloquear"):
        st.session_state.authenticated = False
        st.rerun()

    # Título Principal
    st.title(f"🚀 {escolha_dia}")

    # Lógica de Carregamento de Conteúdo (Caminhos Corrigidos para GitHub/Streamlit Cloud)
    def load_content(day):
        # O caminho agora é relativo ao local onde o app.py está sendo executado
        base_path = os.path.dirname(__file__)
        content_dir = os.path.join(base_path, "content")
        
        file_map = {
            1: "curso_cortex_ia_dia_01_final_v3.md",
            2: "curso_cortex_ia_dia_02_final_v3.md",
        }
        
        if day == 21:
            parts = ["curso_cortex_ia_dia_21_intensivao_parte_1.md", 
                     "curso_cortex_ia_dia_21_intensivao_parte_2.md", 
                     "curso_cortex_ia_dia_21_intensivao_parte_3.md"]
            full_content = ""
            for p in parts:
                path = os.path.join(content_dir, p)
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        full_content += f.read() + "\n\n---\n\n"
            return full_content if full_content else "Conteúdo do Intensivão não encontrado."

        if day in file_map:
            filename = file_map[day]
        else:
            filename = f"curso_cortex_ia_dia_{day:02d}_final.md"
            
        path = os.path.join(content_dir, filename)
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return f"Conteúdo do Dia {day} não encontrado no caminho: {path}"

    content = load_content(dia_num)

    # Layout de Colunas (Conteúdo | Ferramentas)
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(content)
        
        st.markdown("---")
        if st.button("✅ Marcar Dia como Concluído"):
            if dia_num < 21:
                st.session_state.dia_atual = dia_num + 1
                st.success(f"Parabéns! Dia {dia_num} concluído. Prepare-se para o Dia {dia_num + 1} amanhã.")
                st.balloons()
            else:
                st.success("VOCÊ CONCLUIU A JORNADA CORTEX IA! O MUNDO É SEU.")
                st.balloons()

    with col2:
        # Cronômetro de Leitura
        st.markdown('<div class="timer-box">⏱️ Tempo Sugerido: 15:43</div>', unsafe_allow_html=True)
        
        if st.button("▶️ Iniciar Cronômetro"):
            placeholder = st.empty()
            seconds = 15 * 60 + 43
            if dia_num == 21: seconds = 60 * 60 # 1 hora para o intensivão
            
            while seconds > 0:
                mins, secs = divmod(seconds, 60)
                timer = f'{mins:02d}:{secs:02d}'
                placeholder.markdown(f'<div class="timer-box">⏳ Restante: {timer}</div>', unsafe_allow_html=True)
                time.sleep(1)
                seconds -= 1
            st.warning("Tempo de leitura concluído! Agora foque nos exercícios.")

        st.markdown("---")
        st.subheader("📝 Laboratório de Aprendizado")
        st.write("Registre seus Brain-links e exercícios de Feynman aqui:")
        
        user_notes = st.text_area("Suas anotações do dia:", 
                                  value=st.session_state.exercicios.get(dia_num, ""),
                                  height=300,
                                  key=f"notes_{dia_num}")
        
        if st.button("💾 Salvar Anotações"):
            st.session_state.exercicios[dia_num] = user_notes
            st.success("Anotações salvas com sucesso!")

    # Rodapé
    st.markdown("---")
    st.markdown("<center>Cortex IA © 2026 - Domine a si mesmo. Domine o mundo.</center>", unsafe_allow_html=True)
