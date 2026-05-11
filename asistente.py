#!/usr/bin/env python3
"""
asistente.py — Asistente CLI con streaming y gestión de historial.
Uso: python asistente.py
"""
 
from dotenv import load_dotenv
load_dotenv()  # Carga .env antes de importar groq
 
from groq import Groq
import time
import sys
import os

#importamos los errores
from groq import (
    Groq,
    RateLimitError,
    APIConnectionError,
    APIStatusError
)
 
 
# ─── Configuración ────────────────────────────────────────────────────────────
 
MODELO = os.getenv('MODEL')
MAX_TOKENS = 300
MAX_REINTENTOS = 3
 
SYSTEM_PROMPT = """Eres un asistente inteligente y amigable.
Responde siempre en español, de forma clara y concisa.
Si el usuario pregunta sobre código, muéstralo con bloques de código.
Si no conoces algo con certeza, indícalo claramente."""
 
# Colores ANSI para la terminal
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GREY   = "\033[90m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
 
 
# ─── Cliente ─────────────────────────────────────────────────────────────────
 
def crear_cliente() -> Groq | None:
    """Crea el cliente de Groq. Verifica que la clave exista."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        print(f"{RED}❌ Error: GROQ_API_KEY no encontrada.{RESET}")
        print(f"   Crea un archivo .env con: GROQ_API_KEY=tu-clave")
        return None
    return Groq(api_key=api_key)
 
 
# ─── Lógica de chat ──────────────────────────────────────────────────────────
 
def chat(
    client: Groq,
    historial: list,
    mensaje: str,
    tokens_totales: dict
) -> bool:
    """
    Envía un mensaje con streaming y actualiza historial y contador de tokens.
    Devuelve True si tuvo éxito, False si falló definitivamente.
    """
    historial.append({"role": "user", "content": mensaje})
    texto_acumulado = ""
    
    print(f"\n{GREEN}{BOLD}🤖 Asistente:{RESET} ", end="", flush=True)
    
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            stream = client.chat.completions.create(
                model=MODELO,
                max_tokens=MAX_TOKENS,
                messages=historial,
                stream=True
            )
            for chunk in stream:
                contenido = chunk.choices[0].delta.content or "" 
                print(contenido, end="", flush=True)
                texto_acumulado += contenido
                
                if chunk.usage:    
                    # Capturar uso de tokens
                    tokens_totales["entrada"] += chunk.usage.prompt_tokens
                    tokens_totales["salida"]  += chunk.usage.completion_tokens
                
            print()  # Salto de línea al terminar la respuesta
            
            # Guardar respuesta en historial
            historial.append({"role": "assistant", "content": texto_acumulado})
            return True
        
        except RateLimitError:
            espera = 2 ** intento
            print(f"\n{YELLOW}⏳ Límite de velocidad. Esperando {espera}s...{RESET}")
            time.sleep(espera)
            texto_acumulado = ""  # Reiniciar para el siguiente intento
        
        except APIConnectionError:
            if intento < MAX_REINTENTOS:
                print(f"\n{YELLOW}🌐 Sin conexión. Reintentando...{RESET}")
                time.sleep(2 ** intento)
                texto_acumulado = ""
            else:
                print(f"\n{RED}❌ No se pudo conectar a la API.{RESET}")
                historial.pop()  # Quitar el mensaje del usuario si falló
                return False
        
        except APIStatusError as e:
            print(f"\n{RED}❌ Error de API ({e.status_code}).{RESET}")
            historial.pop()
            return False
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}(Generación interrumpida){RESET}")
            if texto_acumulado:
                historial.append({"role": "assistant", "content": texto_acumulado})
            return True
    
    print(f"\n{RED}❌ Se agotaron los reintentos.{RESET}")
    historial.pop()
    return False
 
 
# ─── Comandos especiales ─────────────────────────────────────────────────────
 
def manejar_comando(
    comando: str,
    historial: list,
    tokens_totales: dict
) -> bool:
    """
    Procesa comandos especiales. Devuelve True si debe continuar,
    False si el usuario quiere salir.
    """
    cmd = comando.lower().strip()
    
    if cmd in ("/salir", "/exit", "/q"):
        total = tokens_totales["entrada"] + tokens_totales["salida"]
        print(f"\n{CYAN}Sesión terminada.{RESET}")
        print(f"{GREY}Tokens usados en la sesión: "
              f"entrada={tokens_totales['entrada']}, "
              f"salida={tokens_totales['salida']}, "
              f"total={total}{RESET}")
        return False
    
    elif cmd == "/limpiar":
        historial.clear()
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{CYAN}Historial limpiado. Nueva conversación iniciada.{RESET}\n")
    
    elif cmd == "/historial":
        if not historial:
            print(f"{GREY}El historial está vacío.{RESET}")
        else:
            print(f"\n{CYAN}── Historial ({len(historial)} mensajes) ──{RESET}")
            for i, msg in enumerate(historial):
                rol = "👤" if msg["role"] == "user" else "🤖"
                preview = msg["content"][:100].replace("\n", " ")
                if len(msg["content"]) > 100:
                    preview += "..."
                print(f"  [{i+1}] {rol} {preview}")
            print()
    
    elif cmd == "/tokens":
        total = tokens_totales["entrada"] + tokens_totales["salida"]
        print(f"{GREY}Tokens en esta sesión — "
              f"entrada: {tokens_totales['entrada']}, "
              f"salida: {tokens_totales['salida']}, "
              f"total: {total}{RESET}")
    
    elif cmd == "/ayuda":
        print(f"""
{CYAN}Comandos disponibles:{RESET}
  /salir     → Terminar el programa
  /limpiar   → Borrar el historial y empezar de nuevo
  /historial → Ver todos los mensajes de la sesión
  /tokens    → Ver tokens usados en la sesión
  /ayuda     → Mostrar este mensaje
""")
    
    else:
        print(f"{YELLOW}Comando desconocido: '{comando}'. Escribe /ayuda.{RESET}")
    
    return True
 
 
# ─── Programa principal ───────────────────────────────────────────────────────
 
def main():
    """Función principal del asistente."""
    # Limpiar pantalla
    os.system("cls" if os.name == "nt" else "clear")
    
    # Banner de bienvenida
    print(f"""{CYAN}{BOLD}
╔══════════════════════════════════════════╗
║        🤖 Asistente IA — CLI             ║
║   Powered by Claude (Groq)          ║
╚══════════════════════════════════════════╝{RESET}
Modelo: {MODELO}
Escribe {BOLD}/ayuda{RESET} para ver los comandos disponibles.
Usa {BOLD}Ctrl+C{RESET} para interrumpir una respuesta.
Usa {BOLD}Ctrl+D{RESET} o {BOLD}/salir{RESET} para terminar.
""")
    
    # Inicializar cliente
    client = crear_cliente()
    if client is None:
        sys.exit(1)
    
    # Estado de la sesión
    historial: list = [{'role':'system', 'content':SYSTEM_PROMPT}] # Iniciamos con el System Prompt
    tokens_totales: dict = {"entrada": 0, "salida": 0}
    
    # Bucle principal
    while True:
        try:
            entrada = input(f"\n{BOLD}👤 Tú:{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D o Ctrl+C en el input → salir limpiamente
            print()
            manejar_comando("/salir", historial, tokens_totales)
            break
        
        if not entrada:
            continue
        
        # Comandos especiales (empiezan con /)
        if entrada.startswith("/"):
            continuar = manejar_comando(entrada, historial, tokens_totales)
            if not continuar:
                break
            continue
        
        # Validación básica
        if len(entrada) > 20000:
            print(f"{YELLOW}⚠ Mensaje demasiado largo (máx. 20000 caracteres).{RESET}")
            continue
        
        # Enviar mensaje
        chat(client, historial, entrada, tokens_totales)
 
 
if __name__ == "__main__":
    main()
