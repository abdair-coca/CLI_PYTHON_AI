# 02_parametros.py
 
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

import os
 
client = Groq(
    api_key=os.getenv("API_KEY")
)
 
# Definimos el system prompt como string separado (buena práctica)
SYSTEM_PROMPT = """Eres un asistente especializado en programación Python.
Responde siempre en español.
Cuando muestres código, usa siempre bloques de código con ```python.
Si no sabes algo con certeza, dilo explícitamente.
Sé conciso: máximo 5 oraciones de explicación antes de mostrar el código."""

respuesta = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "¿Cómo ordeno una lista de diccionarios por una clave específica?"
        }
    ],
    # La respuesta sera muy impredecible
    temperature=1.0,
    # Respuesta medianamente
    max_tokens=300,
    
    # Stream: Permite mostrar el mensaje mientras se genera
    stream=True
)
 

#print(respuesta.choices[0].message.content) ---Respuesta sin Stream

#--- Chunk es un fragmento de texto --- 
# stream hace que envie chunks mientras la respuesta se completa
for chunk in respuesta:
    print(chunk.choices[0].delta.content or "", end="") #mostramos cada chunk
