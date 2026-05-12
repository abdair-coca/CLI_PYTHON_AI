from groq import Groq

# python-dotenv lee el archivo .env y carga las variables en os.environ
from dotenv import load_dotenv
load_dotenv()

import os

client = Groq(
    api_key=os.getenv("API_KEY")
)
print()
while True:
    mensaje = input("Tu:")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f'{mensaje}',
            }
        ],
        model=os.getenv("MODEL"),
    )
    print(chat_completion)
    print(f'ChatBot: {chat_completion.choices[0].message.content}')