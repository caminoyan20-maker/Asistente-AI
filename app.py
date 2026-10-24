import time
from google import genai
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="SAY - Asistente de IA", page_icon="⚡", layout="centered")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ SAY AI")
    st.caption("Tu asistente inteligente personal")
    st.markdown("---")
    
    # Botón para limpiar conversación
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("💡 **Tip:** Puedes preguntarle a SAY sobre tareas, resúmenes o explicaciones.")

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

# Mensaje inicial si el chat está vacío
if len(st.session_state.messages) == 0:
    st.info("👋 Escribe tu primera pregunta abajo para comenzar a chatear.")

# 3. Mostrar el historial en pantalla
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 4. Entrada del usuario y generación de respuesta
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("SAY está procesando tu respuesta..."):
            response_text = None
            max_intentos = 3
            
            # Reintentos automáticos si el servidor está saturado
            for intento in range(max_intentos):
                try:
                    res = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt,
                        config={
                            "system_instruction": "Te llamas SAY. Eres un asistente virtual inteligente, amable y claro. Responde SIEMPRE en español con buen formato."
                        }
                    )
                    response_text = res.text
                    break  # Si responde con éxito, salimos del bucle
                except Exception as e:
                    if ("503" in str(e) or "UNAVAILABLE" in str(e)) and intento < max_intentos - 1:
                        time.sleep(2)  # Espera 2 segundos antes de reintentar
                    else:
                        st.warning("⚠️ Los servidores de Google están experimentando alta demanda. Vuelve a enviar tu mensaje en unos segundos.")

            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
                
