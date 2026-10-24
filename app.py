from google import genai
import streamlit as st

st.title("🤖 SAY")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    st.error("No se encontró la clave GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe algo para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("SAY está pensando..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config={
                        "system_instruction": "Te llamas SAY. Eres un asistente virtual servicial y amable. Responde SIEMPRE en español."
                    }
                )
                st.markdown(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
    except Exception as e:
        st.warning("⚠️ Ocurrió alta demanda en el servidor. Vuelve a enviar tu mensaje en unos segundos.")
        
