# AI Chat Python - Asistente CLI con Groq

Proyecto de aprendizaje para interactuar con modelos de lenguaje grandes (LLMs) mediante la API de Groq, implementando un asistente de chat por línea de comandos con características avanzadas.

## Descripcion

Este proyecto teacha los conceptos fundamentals del uso de APIs de LLMs en Python, partiendo desde una simple llamada hasta un asistente completo con streaming, gestión de errores, historial de conversación y herramientas especializadas como traductor y analizador de codigo.

## Caracteristicas

- **Chat interactivo CLI** con streaming en tiempo real
- **Gestión de historial** de conversación con opciones de guardado y resumen
- **Manejo robusto de errores** con reintentos automáticos y backoff exponencial
- **System prompts** configurables para personalizar el comportamiento del modelo
- **Control de parametros** como temperature, max_tokens y model selection
- **Herramientas adicionales**: traductor batch y analizador de codigo
- **Colores en terminal** para mejor experiencia de usuario

## Requisitos

- Python 3.10+
- Cuenta en [Groq](https://console.groq.com/) con API key
- Archivo `.env` con las variables de configuración

## Instalacion

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual (recomendado)**

```bash
python -m venv venv
```

3. **Activar el entorno virtual**

En Windows:
```bash
.\venv\Scripts\activate
```

En Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install groq python-dotenv
```

## Configuracion

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
API_KEY=tu_api_key_de_groq
MODEL=llama-3.3-70b-versatile
```

Para obtener tu API key:
1. Ve a [Groq Console](https://console.groq.com/)
2. Crea una cuenta o inicia sesión
3. Genera una nueva API key en la sección de API Keys

## Estructura del Proyecto

```
ai-chat-python/
├── asistente.py          # Asistente CLI principal con todas las features
├── groqp.py             # Ejemplo basico de chat
├── 01-PrimeraLlamada.py # Tutorial: primera llamada a la API
├── 02-Parametros.py     # Tutorial: parametros del modelo
├── 03-Conversacion.py   # Tutorial: gestion de historial
├── 04-Streaming.py      # Tutorial: respuestas en streaming
├── 05-Errores.py        # Tutorial: manejo de errores
├── .env                 # Configuracion (NO compartir)
├── .gitignore           # Archivos a ignorar en git
├── EjrPropuestos/
│   ├── 01-Exercise/
│   │   └── traductor.py # Traductor batch de archivos
│   ├── 03-Exercise/
│   │   └── assistent.py # Asistente con historial en archivo
│   └── 04-Exercise/
│       └── analyzer.py  # Analizador de codigo Python
```

## Uso

### Asistente Principal

Ejecutar el asistente interactivo:

```bash
python asistente.py
```

Comandos disponibles:
- `/salir` - Terminar el programa
- `/limpiar` - Borrar historial y empezar nueva conversación
- `/historial` - Ver todos los mensajes de la sesión
- `/tokens` - Ver tokens usados en la sesión
- `/ayuda` - Mostrar ayuda

### Tutoriales

Los archivos numerados (01-05) son ejercicios guiados que cubren conceptos específicos:

```bash
python 01-PrimeraLlamada.py  # Primera llamada basica
python 02-Parametros.py     # Parametros y streaming
python 03-Conversacion.py   # Historial de conversación
python 04-Streaming.py      # Streaming en tiempo real
python 05-Errores.py       # Manejo de errores robusto
```

### Ejercicios Propuestos

**Traductor (Ejercicio 1)**

```bash
# Crear archivo entrada.txt con texto a traducir
python EjrPropuestos/01-Exercise/traductor.py
```

**Asistente con Memoria (Ejercicio 3)**

```bash
python EjrPropuestos/03-Exercise/assistent.py
# Comandos adicionales: /guardar, /resumir
```

**Analizador de Codigo (Ejercicio 4)**

```bash
python EjrPropuestos/04-Exercise/analyzer.py --explicar archivo.py
python EjrPropuestos/04-Exercise/analyzer.py --mejorar archivo.py
python EjrPropuestos/04-Exercise/analyzer.py --bugs archivo.py
```

## Conceptos Aprendidos

- Integración con APIs de LLMs (Groq SDK)
- Configuración de modelos (temperature, max_tokens)
- System prompts y contexto de conversación
- Streaming de respuestas
- Gestión de historial y memoria conversacional
- Manejo de errores (RateLimitError, APIConnectionError, APIStatusError)
- Logging y monitoreo de uso de tokens
- Creación de herramientas CLI especializadas

## Notas Importantes

- Nunca compartas tu archivo `.env` ni tu API key
- Los modelos de Groq tienen limites de rate; el código incluye reintentos automáticos
- El uso de tokens genera costos; monitorea el consumo con `/tokens`
- El proyecto está diseñado para aprendizaje; mejora y personalízalo según necesidades

## Recursos

- [Documentación Groq API](https://console.groq.com/docs)
- [Groq SDK Python](https://github.com/groq/groq-python)
- [Modelos disponibles](https://console.groq.com/docs/models)