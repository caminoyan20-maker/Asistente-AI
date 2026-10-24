from google import genai
import streamlit as st

st.set_page_config(page_title="SAY - Asistente de IA", page_icon="⚡", layout="centered")

with st.sidebar:
    st.title("⚡ SAY AI")
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("✨ Hola, soy SAY")
st.subheader("¿En qué te puedo ayudar hoy?")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    st.error("No se encontró la clave GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe un mensaje para SAY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("SAY está procesando tu respuesta..."):
            try:
                # Usamos gemini-2.5-flash para asegurar compatibilidad directa
                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={
                        "system_instruction": "Te llamas SAY. Eres un asistente virtual inteligente, amable y claro. Responde SIEMPRE en español."
                    }
                )
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
            except Exception as e:
                # Esto mostrará el error exacto en la pantalla para solucionarlo al instante
                st.error(f"❌ Error técnico detectado: {e}")
                
