from google import genai
import streamlit as st

# Configuración de página
st.set_page_config(page_title="SAY - Asistente de IA", page_icon="⚡", layout="centered")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ SAY AI")
    st.caption("Tu asistente inteligente personal")
    st.markdown("---")
    
    # Botón para reiniciar/limpiar la conversación
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("💡 **Tip:** Puedes preguntarle a SAY sobre tareas, resúmenes, ideas creativas o explicaciones.")

# --- ENCABEZADO DE LA APP ---
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
    st.info("👋 Escribe tu primera pregunta en la casilla inferior para comenzar a chatear.")

# 3. Mostrar el historial en pantalla con iconos personalizados
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 4. Entrada del usuario y generación de respuesta
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Generar respuesta con animación
    try:
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("SAY está procesando tu respuesta..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config={
                        "system_instruction": "Te llamas SAY. Eres un asistente virtual altamente inteligente, amable y claro. Responde SIEMPRE en español con excelente formato usando negrillas o puntos cuando sea necesario."
                    }
                )
                st.markdown(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
    except Exception as e:
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            st.warning("⚠️ Los servidores de Google están experimentando alta demanda. Vuelve a enviar tu mensaje en unos segundos.")
        else:
            st.error(f"Ocurrió un error: {e}")
            
