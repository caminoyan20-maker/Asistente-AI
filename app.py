import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="SAY AI", page_icon="⚡")

st.title("⚡ SAY AI")
st.subheader("Tu asistente inteligente personal")
st.caption("💡 Tip: Pregúntale a SAY cualquier duda, resumen o tarea que necesites.")

# 2. Configuración de la API Key desde los Secrets de Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Usamos gemini-1.5-flash para alta velocidad y límites estándar del nivel gratuito
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("⚠️ No se encontró la API Key en los Secrets o no es válida.")
    st.stop()

# 3. Inicializar el historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Mostrar los mensajes previos del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Entrada de usuario y generación de respuesta
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    # Guardar y mostrar el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta con manejo de errores
    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                st.error("❌ Se ha superado el límite de consultas por día/minuto de la API Key actual. Por favor, intenta de nuevo más tarde o revisa tu clave en Google AI Studio.")
            else:
                st.error(f"❌ Ocurrió un error al conectar con Gemini: {e}")
                
