    try:
        # Intentamos consultar el modelo principal
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        with st.chat_message("assistant"):
            st.markdown(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
    except Exception as e:
        # Si el servidor de Google está saturado (Error 503/429), le damos un mensaje amigable
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            st.warning("⚠️ Los servidores de Gemini están experimentando alta demanda en este momento. Por favor, reintenta enviar tu mensaje en unos segundos.")
        else:
            st.error(f"Ocurrió un error al consultar a Gemini: {e}")
            
