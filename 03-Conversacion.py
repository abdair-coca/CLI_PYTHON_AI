from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()

client = Groq(
    api_key=os.getenv("API_KEY")
)

historial = []

system = "Eres un asistente amigable. Responde siempre en español y de forma concisa."

historial.append(
    {
        'role': 'system',
        'content': system
    }
)

def chat(mensajeUser: str) -> str:
    historial.append({
        'role': 'user',
        'content': mensajeUser
    })
    
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=historial,
        max_tokens=20
    )
    
    textResponse = response.choices[0].message.content
    
    historial.append(
        {
            'role': 'assistant',
            'content': textResponse
        }
    )
    
    return textResponse

print("Turno 1:", chat("Me llamo Abdair y estoy aprendiendo Python."))
print()
print("Turno 2:", chat("¿Recuerdas cómo me llamo?"))
print()
print("Turno 3:", chat("¿Qué te dije que estaba aprendiendo?"))
print()
print(f"Tamaño del historial: {len(historial)} mensajes")

def mostrar_historial():
    """Imprime el historial formateado para debugging."""
    print("\n" + "="*50 + " HISTORIAL " + "="*50)
    for i, msg in enumerate(historial[1::]):
        rol = "👤 Usuario" if msg["role"] == "user" else "🤖 Asistente"
        print(f"\n[{i+1}] {rol}:")
        print(f"    {msg['content'][:200]}{'...' if len(msg['content']) > 200 else ''}")
    print("="*111 + "\n")
 
mostrar_historial()

def chat_con_ventana(mensaje_usuario: str, max_mensajes: int = 10) -> str:
    """Versión del chat que mantiene solo los últimos N mensajes."""
    historial.append({"role": "user", "content": mensaje_usuario})
    
    # Mantener solo los últimos max_mensajes mensajes
    # (siempre en pares: user + assistant)
    historial_recortado = historial[-max_mensajes:]
    
    # Asegurar que el primero sea siempre "user"
    if historial_recortado and historial_recortado[0]["role"] == "assistant":
        historial_recortado = historial_recortado[1:]
    
    respuesta = client.messages.create(
        model=os.getenv("MODEL"),
        max_tokens=20,
        system=system,
        messages=historial_recortado
    )
    
    texto = respuesta.choices[0].message.content
    historial.append({"role": "assistant", "content": texto})
    return texto
