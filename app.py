import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(
    page_title="SAY AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Control de Estado para la Pantalla de Bienvenida (Intro)
if "intro_visto" not in st.session_state:
    st.session_state.intro_visto = False

# Estilos CSS Cyberpunk / Neón optimizados
st.markdown("""
    <style>
    .stApp {
        background-color: #050b14;
        color: #e0f7fc;
    }
    .hero-container {
        text-align: center;
        padding: 10px 0;
    }
    .neon-title {
        font-size: 3rem;
        font-weight: 800;
        color: #00e5ff;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.8), 
                     0 0 20px rgba(0, 229, 255, 0.5), 
                     0 0 30px rgba(0, 229, 255, 0.3);
        margin-bottom: 0px;
        letter-spacing: 3px;
    }
    .neon-subtitle {
        font-size: 0.9rem;
        color: #80d8ff;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-top: 5px;
        margin-bottom: 20px;
        text-shadow: 0 0 8px rgba(128, 216, 255, 0.6);
    }
    .stChatMessage {
        background-color: rgba(13, 27, 42, 0.95) !important;
        border: 1px solid rgba(0, 229, 255, 0.4);
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
    }
    /* Contenedor estilo marco neón para la segunda imagen */
    .neon-frame {
        border: 2px solid rgba(0, 229, 255, 0.6);
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.35), inset 0 0 15px rgba(0, 229, 255, 0.15);
        background: rgba(5, 11, 20, 0.85);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Botones flotantes de desplazamiento rápido en las esquinas
st.markdown("""
    <div style="position: fixed; top: 70px; right: 20px; z-index: 9999;">
        <button onclick="window.scrollTo({top: 0, behavior: 'smooth'});" style="background: #00e5ff; color: #050b14; border: none; border-radius: 50%; width: 40px; height: 40px; font-weight: bold; cursor: pointer; box-shadow: 0 0 12px #00e5ff;">⬆️</button>
    </div>
    <div style="position: fixed; bottom: 90px; right: 20px; z-index: 9999;">
        <button onclick="window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});" style="background: #00e5ff; color: #050b14; border: none; border-radius: 50%; width: 40px; height: 40px; font-weight: bold; cursor: pointer; box-shadow: 0 0 12px #00e5ff;">⬇️</button>
    </div>
""", unsafe_allow_html=True)

# 3. Configuración de API Keys múltiples
api_keys = []
if "GEMINI_API_KEYS" in st.secrets:
    api_keys = st.secrets["GEMINI_API_KEYS"]
elif "GEMINI_API_KEY" in st.secrets:
    api_keys = [st.secrets["GEMINI_API_KEY"]]

if not api_keys:
    st.error("⚠️ No se encontró ninguna API Key configurada en los Secrets.")
    st.stop()

# 4. PANTALLA DE BIENVENIDA (Primera Imagen: Cerebro Holográfico)
if not st.session_state.intro_visto:
    st.markdown("""
        <div class='hero-container'>
            <div class='neon-title'>SAY AI</div>
            <div class='neon-subtitle'>Quantum AI Search Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        intro_img = Image.open("1792876050319.jpg")
        st.image(intro_img, use_container_width=True)
    except Exception:
        st.info("⚡ Cargando núcleo cuántico de bienvenida...")
        
    st.write("")
    if st.button("🚀 Iniciar Sistema SAY", use_container_width=True):
        st.session_state.intro_visto = True
        st.rerun()
    st.stop()

# 5. INTERFAZ PRINCIPAL (Segunda Imagen dentro del marco y diseño completo)
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control SAY")
    if st.button("🏠 Ver Intro Nuevamente", use_container_width=True):
        st.session_state.intro_visto = False
        st.rerun()
    if st.button("🗑️ Limpiar Historial de Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Marco estilo neón con la segunda imagen integrada exactamente como pediste
st.markdown("<div class='neon-frame'>", unsafe_allow_html=True)
try:
    main_img = Image.open("1792876108417.jpg")
    st.image(main_img, use_container_width=True)
except Exception:
    pass

st.markdown("""
    <div class="hero-container" style="padding: 5px 0 0 0;">
        <div class="neon-title" style="font-size: 2.2rem;">SAY AI</div>
        <div class="neon-subtitle">Búsqueda Cuántica Multimodal</div>
    </div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Opción compacta para subir imágenes desde la galería justo arriba del chat
with st.expander("📁 Adjuntar imagen desde la galería para consultar", expanded=False):
    uploaded_file = st.file_uploader("Selecciona una imagen (PNG, JPG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img_preview = Image.open(uploaded_file)
    st.image(img_preview, width=180, caption="Imagen lista para enviar")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"] is not None:
            st.image(message["image"], width=220)

# Entrada de chat con memoria y soporte multimodal corregido
if prompt := st.chat_input("Escribe tu consulta a SAY..."):
    image_pil = None
    if uploaded_file is not None:
        image_pil = Image.open(uploaded_file)
        uploaded_file = None # Limpiar después de capturar

    st.session_state.messages.append({"role": "user", "content": prompt, "image": image_pil})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if image_pil:
            st.image(image_pil, width=220)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⚡ Analizando con el núcleo cuántico...")
        
        texto_final = ""
        exito = False
        
        for key in api_keys:
            try:
                genai.configure(api_key=key)
                # Forzar nombre de modelo limpio y estándar sin prefijos extraños
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                content_inputs = []
                if image_pil:
                    content_inputs.append(image_pil)
                content_inputs.append(prompt)
                
                gemini_history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1] if m["content"]
                ]
                
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(content_inputs, stream=True)
                
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
                    texto_final = f"❌ Error de conexión: {e}"
                    placeholder.markdown(texto_final)
                    exito = True
                    break
                    
        if not exito:
            texto_final = "❌ Todas las claves configuradas han alcanzado su límite diario."
            placeholder.markdown(texto_final)
            
        st.session_state.messages.append({"role": "assistant", "content": texto_final, "image": None})
        
