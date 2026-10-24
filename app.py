import streamlit as st
import google.generativeai as genai

# 1. Configuración de la interfaz
st.set_page_config(page_title="SAY AI", page_icon="⚡")

st.title("⚡ SAY AI")
st.subheader("Tu asistente inteligente personal")
st.caption("💡 Tip: Pregúntale a SAY cualquier duda, resumen o tarea que necesites.")

# 2. Configuración de la API Key y Modelo
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Modelo requerido por la API
    model = genai.GenerativeModel("gemini-3.8-flash")
except Exception as e:
    st.error("⚠️ No se encontró la API Key en los Secrets o no está configurada correctamente.")
    st.stop()

# 3. Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Mostrar el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Entrada del usuario y generación de respuesta
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                st.error("❌ Se ha alcanzado el límite diario o temporal de consultas. Intenta de nuevo más tarde o genera una API Key nueva en Google AI Studio.")
            else:
                st.error(f"❌ Ocurrió un error: {e}")
                
