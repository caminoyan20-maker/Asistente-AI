import time
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

# 4. Entrada del usuario con reintentos automáticos para evitar el error 503
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("SAY está pensando...")
        
        exito = False
        respuesta_completa = ""
        max_intentos = 5
        
        # Bucle de reintento automático si los servidores están saturados (503)
        for intento in range(max_intentos):
            try:
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config={
                        "system_instruction": "Te llamas SAY. Eres un asistente virtual inteligente, servicial y amable. Responde SIEMPRE en español con excelente formato."
                    }
                )
                
                respuesta_completa = ""
                for chunk in response_stream:
                    if chunk.text:
                        respuesta_completa += chunk.text
                        message_placeholder.markdown(respuesta_completa + "▌")
                
                message_placeholder.markdown(respuesta_completa)
                exito = True
                break  # Si responde con éxito, salimos del bucle
                
            except Exception as e:
                error_str = str(e)
                if ("503" in error_str or "UNAVAILABLE" in error_str) and intento < max_intentos - 1:
                    message_placeholder.markdown(f"⚠️ Alta demanda en el servidor. Reintentando automáticamente (intento {intento+2}/{max_intentos})...")
                    time.sleep(3) # Espera 3 segundos antes de volver a intentar
                else:
                    if not exito:
                        message_placeholder.error(f"❌ No se pudo conectar tras varios intentos. Detalle: {e}")
                        break
                        
        if exito and respuesta_completa:
            st.session_state.messages.append({"role": "assistant", "content": respuesta_completa})
                    
