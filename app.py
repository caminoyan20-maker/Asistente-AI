import streamlit as st
import google.generativeai as genai

# 1. Configuración de la interfaz en Streamlit
st.set_page_config(page_title="SAY AI", page_icon="⚡")

st.title("⚡ SAY AI")
st.subheader("Tu asistente inteligente personal")
st.caption("💡 Tip: Pregúntale a SAY cualquier duda, resumen o tarea que necesites.")

# 2. Configurar la API Key desde los Secrets de Streamlit y definir el modelo
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ⚡ MODELO OPCIÓN A: gemini-1.5-flash (Hasta 1,500 peticiones gratis al día)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("⚠️ No se encontró la API Key en los Secrets o no está configurada correctamente.")
    st.stop()

# 3. Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Mostrar el historial de mensajes guardados
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Capturar la pregunta del usuario y procesar la respuesta
if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    # Guardar y mostrar el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar la respuesta del modelo con control de errores
    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                st.error("❌ Se ha superado el límite temporal de consultas. Intenta de nuevo en unos momentos o renueva tu API Key.")
            else:
                st.error(f"❌ Ocurrió un error: {e}")
                
