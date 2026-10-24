import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(
    page_title="SAY AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Estilos CSS personalizados (Cyberpunk / Neón)
st.markdown("""
    <style>
    .stApp {
        background-color: #050b14;
        color: #e0f7fc;
    }
    .hero-container {
        text-align: center;
        padding: 20px 0;
    }
    .neon-title {
        font-size: 3rem;
        font-weight: 800;
        color: #00e5ff;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.6), 
                     0 0 20px rgba(0, 229, 255, 0.4), 
                     0 0 30px rgba(0, 229, 255, 0.2);
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    .neon-subtitle {
        font-size: 0.95rem;
        color: #80d8ff;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 5px;
        margin-bottom: 25px;
        text-shadow: 0 0 5px rgba(128, 216, 255, 0.4);
    }
    .stChatMessage {
        background-color: rgba(13, 27, 42, 0.8) !important;
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado visual
st.markdown("""
    <div class="hero-container">
        <div class="neon-title">SAY AI</div>
        <div class="neon-subtitle">Quantum AI Search Engine &bull; Illuminating Knowledge</div>
    </div>
""", unsafe_allow_html=True)

# 4. Configuración de API Keys múltiples
api_keys = []
if "GEMINI_API_KEYS" in st.secrets:
    api_keys = st.secrets["GEMINI_API_KEYS"]
elif "GEMINI_API_KEY" in st.secrets:
    api_keys = [st.secrets["GEMINI_API_KEY"]]

if not api_keys:
    st.error("⚠️ No se encontró ninguna API Key configurada en los Secrets.")
    st.stop()

# 5. Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Entrada de chat con streaming ultrarrápido y rotación de claves
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⚡ Conectando al núcleo cuántico...")
        
        texto_final = ""
        exito = False
        
        for key in api_keys:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Generar respuesta en tiempo real (streaming)
                response = model.generate_content(prompt, stream=True)
                texto_final = ""
                for chunk in response:
                    texto_final += chunk.text
                    placeholder.markdown(texto_final + "▌")
                
                placeholder.markdown(texto_final)
                exito = True
                break
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    continue
                else:
                    texto_final = f"❌ Error: {e}"
                    placeholder.markdown(texto_final)
                    exito = True
                    break
                    
        if not exito:
            texto_final = "❌ Todas las claves configuradas han alcanzado su límite diario."
            placeholder.markdown(texto_final)
            
        st.session_state.messages.append({"role": "assistant", "content": texto_final})
        
