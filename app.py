from google import genai
import streamlit as st

st.title("🤖 SAY")

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
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Entrada del usuario y generación de respuesta
if prompt := st.chat_input("Escribe algo para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Mostramos una animación mientras SAY responde
        with st.chat_message("assistant"):
            with st.spinner("SAY está pensando..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config={
                        "system_instruction": "Te llamas SAY. Eres un asistente virtual servicial, inteligente y amable. Responde SIEMPRE en español fluido y claro, independientemente de cómo te pregunte el usuario."
                    }
                )
                st.markdown(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
    except Exception as e:
        if "503" in str(e) or "UNAVAILABLE" in
        
