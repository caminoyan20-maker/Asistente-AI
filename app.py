from google import genai
import streamlit as st

# Configuración de página con icono y título
st.set_page_config(page_title="SAY - Asistente de IA", page_icon="⚡", layout="centered")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ SAY AI")
    st.caption("Tu asistente inteligente personal")
    st.markdown("---")
    
    # Botón para reiniciar conversación
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("💡 **Tip:** Puedes preguntarle a SAY sobre cualquier tema, pedirle resúmenes o ideas creativas.")

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

# 3. Mostrar el historial en pantalla con avatares personalizados
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
        with st.spinner("SAY está pensando..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config={
                        "system_instruction": "Te llamas SAY. Eres un asistente virtual inteligente, servicial y amable. Responde SIEMPRE en español con excelente formato."
                    }
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    st.warning("⚠️ Los servidores están experimentando un pico de alta demanda. Por favor, reintenta enviar tu mensaje en unos segundos.")
                else:
                    st.error(f"Ocurrió un error al consultar a SAY: {e}")
                    
