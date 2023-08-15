import os
import openai
from django.conf import settings
from dotenv import load_dotenv
from elevenlabs import generate, save, set_api_key

load_dotenv()

import requests


class IAServices:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def audio_to_text(self, file_path):
        try:
            audio_file = open(file_path, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript.text

        except Exception as e:
            raise ValueError(f"Error en la transcripcion de audio a texto:\n{e}")

    def gpt_normal(self, text_input, context, id):
        list_context = list(context)
        list_context.append({"role": "user", "content": text_input})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=list_context
            # messages=[
            #     #{"role": "system", "content": "Eres un asistente un poco mal hablado"},
            #     **context,
            #     {"role": "user", "content": text_input}
            # ]
        )

        # guardamos la respuesta en el contexto
        list_context.append(
            {
                "role": completion.choices[0].message["role"],
                "content": completion.choices[0].message["content"],
            }
        )

        # preparamos la respuesta
        response = {
            "text": completion.choices[0].message["content"],
            "id": id,
            "context": list_context,
        }
        return response

    def text_to_voice(self, text, id):
        # extraemos la api key y la usamos
        api_key_eve = os.getenv("ELEVENLABS_API_KEY")
        set_api_key(api_key_eve)

        # generamos audio
        audio = generate(text=text, voice="Josh", model="eleven_multilingual_v1")
        # guardamos el audio
        file_path = os.path.join(settings.MEDIA_ROOT, f"{id}")
        save(audio, file_path)

        return file_path
