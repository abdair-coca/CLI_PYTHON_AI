"""Ejercicio 2 — Generador de tests de Python (Capítulo 4)
Crea generador_tests.py que:
    11.	Reciba el nombre de una función Python y su descripción como entrada del usuario.
    12.	Use un system prompt que instruya al modelo a generar casos de prueba en formato 
    pytest, SOLO el código, sin explicaciones.
    13.	Guarde el código generado en un archivo test_{nombre_funcion}.py.
    14.	Experimenta con stop_sequences=["```"] para que el modelo deje de generar cuando 
    cierra el bloque de código.
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
def crearPy(
    client: Groq,
    function: str,
    descript: str,  
) -> tuple[bool, str]:
    
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            codigo = client.chat.completions.create(
                model=MODELO,
                max_tokens=MAX_TOKENS,
                messages=[
                    {'role':'system',
                     'content':"""
                                Eres un experto en testing de Python.
                                Genera únicamente código pytest válido.
                                Genera tests pytest completos incluyendo imports.
                                NO expliques nada.
                                NO uses markdown.
                                NO escribas ```python.
                                SOLO devuelve código Python.
                                """
                        },
                    {'role': 'user',
                     'content': f"""
                            Genera tests pytest para esta funcion:
                            nombre: {function}
                            
                            description: 
                            {descript}
                     """
                        }
                    ],
                stop=["```"],
                temperature=0.0
            )
            code = codigo.choices[0].message.content
            code = code.replace("```python", "")
            code = code.replace("```", "")
                        
            return True, code
        
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
    """Función principal del test."""
    
    # Inicializar cliente
    client = createClient()
    if client is None:
        print(f"{RED}❌ Error Cliente.{RESET}")
        return
        
    nombreFuncion = input("Nombre de la funcion: \n")
    descript = input("Descripcion: \n")
    nombreFuncion = nombreFuncion.strip().replace(" ", "_")
    
    if not nombreFuncion.strip():
        print(f"{RED} Nombre invalido. {RESET}")
        return
    
    nombreArchivo = f"test_{nombreFuncion}.py"
    
    status, response = crearPy(client, nombreFuncion, descript)
        
    if status:
        archivoNombre = f"test_{nombreFuncion}.py"
        with open(archivoNombre, "w", encoding="utf-8") as salida:  
            salida.write(response)
        
        print(f"{GREEN}✅ Tests guardados en '{archivoNombre}'{RESET}")
    else:
        print(f"{RED} Error de writing.")
    
if __name__ == "__main__":
    main()
