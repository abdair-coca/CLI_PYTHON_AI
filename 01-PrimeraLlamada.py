# 01_primera_llamada.py
 
# python-dotenv lee el archivo .env y carga las variables en os.environ
from dotenv import load_dotenv
load_dotenv()
 
# El SDK de Groq 
from groq import Groq
 
import os
# 1. Crear el cliente
#    Esta es la puerta de entrada a la API.
#    Obtenemos la API_KEY del archivo .env.
client = Groq(
    api_key=os.getenv("API_KEY")
)
 
# 2. Crear el mensaje
#    Este es el corazón de la API. Enviamos una lista de mensajes
#    con el rol "user" (el humano) y el contenido de lo que queremos.
message = client.chat.completions.create(
    model="llama-3.3-70b-versatile",   # El modelo que usaremos (ver Capítulo 4)
    max_tokens=1024,                     # Límite de tokens en la respuesta
    messages=[
        {
            "role": "user",
            "content": "Explícame qué es un token en el contexto de los LLMs, "
                       "en no más de 3 oraciones."
        }
    ]
)
 
# 3. Leer la respuesta
#    message.content es una lista de bloques de contenido.
#    El primer bloque es tipo "text" y tiene el atributo .text con la respuesta.
print("Respuesta del modelo:")
print(message.choices[0].message.content)

# Mostramos message en formato json para ver lo que realmente contiene
#import json
#
#json_response = message.model_dump_json(indent=2)

#print(json_response)


# 4. Ver información de uso
print(f"\nTokens usados — entrada: {message.usage.prompt_tokens}, "
      f"salida: {message.usage.completion_tokens}")

