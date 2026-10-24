from google import genai
import streamlit as st

st.title("🤖 Mi Asistente de IA")

# Obtener la clave API desde Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe algo para tu asistente..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamada a Gemini para respuesta real
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    with st.chat_message("assistant"):
        st.markdown(response.text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )
    
