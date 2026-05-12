from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("API_KEY")
)

print("Respuesta con streaming:\n")

def chat_streaming( historial: list, messUser: str):
    
    historial.append({'role': 'user', 'content': messUser})
    
    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages= historial,
        max_tokens=200,
        stream=True
    )

    respuesta_completa = ""
    
    
    print("🤖 Asistente: ", end="", flush=True)

    for chunk in stream:

        fragmento = chunk.choices[0].delta.content or ""

        respuesta_completa += fragmento

        print(fragmento, end="", flush=True)

    historial.append({
    'role': 'assistant',
    'content': respuesta_completa})

# Prueba
conversacion = []
system = "Eres un asistente de programación. Responde en español."

conversacion.append({'role':'system', 'content':system})
 
chat_streaming(conversacion, "¿Qué es un decorador en Python?")
print()
chat_streaming(conversacion, "Dame un ejemplo práctico del decorador @property.")