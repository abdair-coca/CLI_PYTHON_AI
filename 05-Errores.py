# 05_errores.py
 
from dotenv import load_dotenv
load_dotenv()
import os
import time

 #importamos los errores
from groq import (
    Groq,
    RateLimitError,
    APIConnectionError,
    APIStatusError,
    AuthenticationError
)

client = Groq(
    api_key=os.getenv("API_KEY")
)
 
def llamar_con_reintentos(
    messages: list,
    max_reintentos: int = 3
) -> str | None:
    """
    Llama a la API con manejo de errores y reintentos automáticos.
    Devuelve el texto de la respuesta o None si todos los intentos fallan.
    """
    for intento in range(1, max_reintentos + 1):
        try:
            respuesta = client.chat.completions.create(
                model=os.getenv('MODEL'),
                max_tokens=512,
                messages=messages
            )
            return respuesta.choices[0].message.content
        
        except AuthenticationError:
            # Error de autenticación: no tiene sentido reintentar
            print("❌ Error de autenticación. Verifica tu GROQ_API_KEY en .env")
            return None
        
        except RateLimitError as e:
            # Límite de velocidad: esperar con backoff exponencial
            espera = 2 ** intento  # 2, 4, 8 segundos...
            print(f"⏳ Límite de velocidad alcanzado. Esperando {espera}s "
                  f"(intento {intento}/{max_reintentos})...")
            time.sleep(espera)
        
        except APIStatusError as e:
            # Errores del servidor (5xx): reintentable
            if e.status_code >= 500 and intento < max_reintentos:
                espera = 2 ** intento
                print(f"🔄 Error del servidor ({e.status_code}). "
                      f"Reintentando en {espera}s...")
                time.sleep(espera)
            else:
                print(f"❌ Error de API: {e.status_code} — {e.message}")
                return None
        
        except APIConnectionError:
            # Error de red: sin conexión a internet
            print(f"🌐 Error de conexión. Verifica tu internet. "
                  f"(intento {intento}/{max_reintentos})")
            time.sleep(2 ** intento)
    
    print("❌ Se agotaron todos los reintentos.")
    return None
 
 
# Prueba
resultado = llamar_con_reintentos(
    messages=[{"role": "user", "content": "¿Cuánto es 2 + 2?"}]
)
if resultado:
    print(f"Respuesta: {resultado}")

def validar_mensaje(mensaje: str) -> tuple[bool, str]:
    """
    Valida el mensaje antes de enviarlo a la API.
    Devuelve (es_valido, mensaje_de_error).
    """
    if not mensaje or not mensaje.strip():
        return False, "El mensaje no puede estar vacío."
    
    if len(mensaje.strip()) < 2:
        return False, "El mensaje es demasiado corto."
    
    # Límite de seguridad: ~6000 tokens ≈ 24000 caracteres en español
    if len(mensaje) > 24000:
        return False, f"El mensaje es demasiado largo ({len(mensaje)} caracteres)."
    
    return True, ""
 
 
# Uso en el flujo principal
entrada = input("Tú: ").strip()
valido, error = validar_mensaje(entrada)
 
if not valido:
    print(f"⚠ {error}")
else:
    resultado = llamar_con_reintentos([{"role": "user", "content": entrada}])
    if resultado:
        print(f"Asistente: {resultado}")


# -----Uso de Logging para registrar las llamadas a la API-----
import logging
 
# Configurar el sistema de logging al inicio del script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),              # Muestra en consola
        logging.FileHandler("asistente.log"), # Guarda en archivo
    ]
)
logger = logging.getLogger(__name__)
 
# Dentro de tu función de chat:
def chat_con_log(messages: list) -> str | None:
    logger.info(f"Llamada a API — {len(messages)} mensajes en historial")
    
    try:
        respuesta = client.chat.completions.create(
                model=os.getenv('MODEL'),
                max_tokens=512,
                messages=messages
            )
        logger.info(
            f"Respuesta OK — entrada: {respuesta.usage.prompt_tokens} tokens, "
            f"salida: {respuesta.usage.completion_tokens} tokens"
        )
        return respuesta.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error en llamada a API: {type(e).__name__}: {e}")
        return None

respuesta = chat_con_log([{'role':'user', 'content':'hola'}])
print(respuesta)