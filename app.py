import streamlit as st
from plyer import tts  # O las librerías que uses para la voz

st.title("🤖 Mi Asistente de IA con Voz")

# Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto del usuario
if prompt := st.chat_input("Escribe algo para tu asistente..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del asistente (aquí conectas la lógica de tu IA)
    response = f"Hola, soy tu asistente. Dijiste: {prompt}"
    
    with st.chat_message("assistant"):
        st.markdown(response)
        # Opcional: usar plyer para voz si lo deseas
        # tts.speak(text=response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    
