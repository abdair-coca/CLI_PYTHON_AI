"""
Ejercicio 4 — Analizador de código (Capítulo 6 + todo)
Crea analyzer.py que:
19.	Lea un archivo .py del disco cuya ruta proporciona el usuario.
20.	Lo envíe a Groq con el system prompt: 'Eres un experto en Python. 
Analiza el código y responde en español.'
21.	Ofrezca tres modes vía argumento de línea de comandos (sys.argv): 
--explicar, --mejorar, --bugs.
22.	Use streaming para mostrar el análisis en tiempo real.
23.	Maneje el caso donde el archivo no existe (FileNotFoundError) antes de llamar a la API.
"""

from dotenv import load_dotenv
load_dotenv()
import os
import sys
#importamos los errores
from groq import (
    Groq,
    APIConnectionError,
    APIStatusError
)

# Variables de configuracion
MODELO = os.getenv('MODEL')
MAX_TOKENS = 300

# Colores ANSI para la terminal
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GREY   = "\033[90m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

#────────────────────────Funciones───────────────────────────────
def chat(client: Groq, message:list)-> bool:
    try:
        stream = client.chat.completions.create(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            messages=message,
            stream=True
        )
        for chunk in stream:
            content = (chunk.choices[0].delta.content or "")
            print (content, end="", flush=True)
        print()
        return True
    except APIConnectionError:
        print(f"\n{YELLOW}🌐 Sin conexión. Reintentando...{RESET}")
        print(f"\n{RED}❌ No se pudo conectar a la API.{RESET}")
        return False
    
    except APIStatusError as e:
        print(f"\n{RED}❌ Error de API ({e.status_code}).{RESET}")
        return False
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}(Generación interrumpida){RESET}")
        return True
    
def create_client()->Groq|None:
    api_key = os.getenv("API_KEY")
    if not api_key:
        print(f"{RED}API_KEY invalida, cree o revise la api key{RESET}")
        return None
    return Groq(api_key=api_key)
        
    
def ReadFile(routeFile: str) -> tuple[bool, str]:
    try:
        with open(routeFile, "r", encoding="utf-8") as file:
            return True, file.read()   
    except FileNotFoundError:

        return False, "❌ Archivo no encontrado"

    except PermissionError:

        return False, "❌ Sin permisos para abrir el archivo"

    except Exception as e:

        return False, f"❌ Error: {e}"

def verify_mode(mode:str) -> bool:
    allowCommands = [
        "--explicar",
        "--mejorar",
        "--bugs"
    ]
    return mode in allowCommands
def command_control(mode:str, client:Groq, routeFile:str):
    status, fileRead = ReadFile(routeFile)
    if mode == "--explicar" and status:
        systemPrompt = """
        Eres un experto en Python. 
        Analiza el código y responde en español.
        """
    elif mode == "--mejorar" and status:
        systemPrompt = """
        Eres un experto en Python. 
        Mejora el código y responde en español.
        """
    elif mode == "--bugs" and status:
        systemPrompt = """
        Eres un experto en Python. 
        Encuentra bugs y problemas potenciales en el código.
        """
    else:
        print(f"{RED}{fileRead}{RESET}")
        return
    message =[{
            'role':'system',
            'content':systemPrompt
        },
        {
            'role':'user',
            'content': fileRead
        }]
    chat(client, message)
#────────────────────────Programa Principal───────────────────────────────
def main():
    
    # Banner de bienvenida
    print(f"""{CYAN}{BOLD}
╔══════════════════════════════════════════╗
║        🤖 Analyzer IA — CLI             ║
║              Powered by Groq             ║
╚══════════════════════════════════════════╝{RESET}
Modelo: {MODELO}
Escoger Modo: --explicar || --mejorar || --bugs
Usa {BOLD}Ctrl+D{RESET} o {BOLD}/salir{RESET} para terminar.
""")
    # Inicializar Cliente
    client = create_client()
    if client is None:
        sys.exit(1)
        
    mode = '--explicar'
    routeFile = ""
    mode = sys.argv[1] if len(sys.argv) > 1 else "--explicar"

    routeFile = sys.argv[2] if len(sys.argv) > 2 else ""

    while True:
        if verify_mode(mode) and routeFile.strip():
            command_control(mode, client, routeFile)
            break
        if not verify_mode(mode):
            print(f"{RED}Modo inválido{RESET}")
            return     
                   
        if not routeFile.strip():
            routeFile = input(f"{BOLD}/{mode}/ Ingrese la ruta del archivo:\n{RESET}")
            continue

if __name__ == "__main__":
    main()