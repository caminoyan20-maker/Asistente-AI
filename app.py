from plyer import tts

def hablar(texto):
    """Función para que el teléfono hable usando la voz nativa de Android"""
    try:
        tts.speak(texto)
    except Exception as e:
        print(f"(Aviso de voz: {e})")

def responder_ia(mensaje_usuario):
    """
    Lógica de respuestas de la IA.
    """
    mensaje = mensaje_usuario.lower().strip()
    
    if "hola" in mensaje:
        return "¡Hola! ¿En qué te puedo ayudar hoy?"
    elif "como estas" in mensaje or "cómo estás" in mensaje:
        return "Estoy funcionando al cien por ciento, listo para hablar contigo."
    elif "quien eres" in mensaje or "quién eres" in mensaje:
        return "Soy tu asistente de Inteligencia Artificial ejecutable en Pydroid 3."
    elif "chao" in mensaje or "adios" in mensaje or "salir" in mensaje:
        return "Hasta luego, que tengas un excelente día."
    else:
        return f"Entendí que dijiste: '{mensaje_usuario}'. Aún estoy aprendiendo nuevas respuestas."

# Bucle principal de conversación
print("--- ASISTENTE DE IA INICIADO ---")
print("(Escribe 'salir' para terminar)\n")

# Saludo inicial
saludo = "Hola, soy tu asistente. Escribe un mensaje para comenzar."
print(f"IA: {saludo}")
hablar(saludo)

while True:
    # Capturar mensaje del usuario por teclado
    entrada = input("\nTú: ")
    
    if not entrada.strip():
        continue
        
    # Obtener respuesta de la IA
    respuesta = responder_ia(entrada)
    
    # Mostrar respuesta en texto
    print(f"IA: {respuesta}")
    
    # Responder en voz alta con Android TTS
    hablar(respuesta)
    
    # Salir si el usuario se despide
    if entrada.lower().strip() in ["salir", "chao", "adios"]:
        break
