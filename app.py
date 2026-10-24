from google import genai
import streamlit as st

# Configuración de página
st.set_page_config(page_title="SAY - Asistente de IA", page_icon="⚡", layout="centered")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ SAY AI")
    st.caption("Tu asistente inteligente personal")
    st.markdown("---")
    
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("💡 **Tip:** Pregúntale a SAY cualquier duda, resumen o tarea que necesites.")

# --- ENCABEZADO ---
st.title("✨ Hola, soy SAY")
st.subheader("¿En qué te puedo ayudar hoy?")

# 1. Leer la clave de forma segura desde Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    st.error("No se encontró la clave GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 2. Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Mostrar el historial en pantalla
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 4. Entrada del usuario y generación de respuesta en tiempo real
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Solicitamos la respuesta en flujo (streaming)
            response_stream = client.models.generate_content_stream(
                model="gemini-3.8-flash",
                contents=prompt,
                config={
                    "system_instruction": "Te llamas SAY. Eres un asistente virtual inteligente, servicial y amable. Responde SIEMPRE en español con excelente formato."
                }
            )
            
            # Mostramos el texto conforme va llegando palabra por palabra
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            # Al terminar, fijamos el texto limpio sin el cursor de escritura
            message_placeholder.markdown(full_response)
            
            # Guardamos en el historial
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"⚠️ Ocurrió un error al procesar tu mensaje: {e}")
            
