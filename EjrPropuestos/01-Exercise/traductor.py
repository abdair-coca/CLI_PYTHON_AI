"""Ejercicio 1 — Traductor multiidioma (Capítulos 3 y 4)
Crea traductor.py con las siguientes características:
    7.	Pide al usuario el texto a traducir y el idioma destino.
    8.	Usa un system prompt que instruya al modelo a SOLO devolver 
    la traducción, sin explicaciones adicionales. Prueba con temperature=0.0.
    9.	Compara la longitud en tokens de un texto en español vs su 
    traducción al inglés. ¿Cuál usa más tokens? ¿Por qué tiene sentido?
    10.	Agrega un modo batch: lee un archivo de texto línea a línea y traduce cada una,
    guardando las traducciones en un archivo de salida.
"""

from dotenv import load_dotenv
load_dotenv()
import time
import os
#importamos los errores
from groq import (
    Groq,
    RateLimitError,
    APIConnectionError,
    APIStatusError
)
 
MODELO = os.getenv('MODEL')
MAX_TOKENS = 300
MAX_REINTENTOS = 3
 
 
# Colores ANSI para la terminal
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GREY   = "\033[90m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def createClient () -> Groq | None:
    api_key = os.getenv("API_KEY")
    if not api_key:
        print(f"{RED}❌ Error: GROQ_API_KEY no encontrada.{RESET}")
        print(f"   Crea un archivo .env con: GROQ_API_KEY=tu-clave")
        return None
    return Groq(api_key=api_key)
def traducir(
    client: Groq,
    mensaje: str,
    cantTok: dict,
    language: str   
) -> tuple[bool, str]:
    """
    Traducimos el texto enviado / No es necesario Stream
    """
    
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            result = client.chat.completions.create(
                model=MODELO,
                max_tokens=MAX_TOKENS,
                messages=[
                    {'role':'system',
                     'content':f'Eres un traductor, solo traduce el texto a este lenguaje: {language}, no des explicaciones solo traduce y ya, solo enviame la traduccion sin ningun otro texto mas'
                        },
                    {'role': 'user',
                     'content': mensaje
                        }
                    ],
                temperature=0.0
            )
            traduccion = result.choices[0].message.content
            
            #Guardamos los tokenks usados
            cantTok["entrada"] += result.usage.prompt_tokens
            cantTok["salida"]  += result.usage.completion_tokens
            
            return True, traduccion
        
        except RateLimitError:
            espera = 2 ** intento
            print(f"\n{YELLOW}⏳ Límite de velocidad. Esperando {espera}s...{RESET}")
            time.sleep(espera)
        
        except APIConnectionError:
            if intento < MAX_REINTENTOS:
                print(f"\n{YELLOW}🌐 Sin conexión. Reintentando...{RESET}")
                time.sleep(2 ** intento)
            else:
                print(f"\n{RED}❌ No se pudo conectar a la API.{RESET}")
                return False, ""
        
        except APIStatusError as e:
            print(f"\n{RED}❌ Error de API ({e.status_code}).{RESET}")
            return False, ""
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}(Generación interrumpida){RESET}")
    
    print(f"\n{RED}❌ Se agotaron los reintentos.{RESET}")
    return False, ""


def main():
    """Función principal del traductor."""
    
    # Banner de bienvenida
    print(f"""{CYAN}{BOLD}
╔══════════════════════════════════════════╗
║              🤖 Traductor                ║
║            Powered by Groq               ║
╚══════════════════════════════════════════╝{RESET}
""")
    
    # Inicializar cliente
    client = createClient()
    if client is None:
        print(f"{RED}❌ Error Cliente.{RESET}")
        return
        
    language = input("A que idioma desea traducir?: \n")
    
    if not language.strip():
        language = "English"
    
    archivo_entrada = "entrada.txt"
    archivo_salida = "salida.txt"
    cantTok : dict = {"entrada": 0, "salida": 0}

    with open(archivo_entrada, "r", encoding="utf-8") as entrada:
        lineas = entrada.readlines()
        
    traducciones = []

    for linea in lineas:

        texto = linea.strip()

        # Ignorar líneas vacías
        if not texto:
            traducciones.append("")
            continue
            
        status, response = traducir(client, texto, cantTok, language)
        
        if status:
            traducciones.append(response)
        else: 
            break
    with open(archivo_salida, "w", encoding="utf-8") as salida:

        for traduccion in traducciones:
            salida.write(traduccion + "\n")
            
        salida.write(
            f"\n\nEspañol tokens: {cantTok['entrada']}"
            f"\n{language} tokens: {cantTok['salida']}"
        )            
    print(f"Traduccion guardada en el archivo '{archivo_salida}'")
if __name__ == "__main__":
    main()
