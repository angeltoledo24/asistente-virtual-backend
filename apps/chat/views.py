from typing import Any
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from django.conf import settings
from .services.ia_services import IAServices
import json
import os


class AudioUploadView(APIView, IAServices):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def post(
        self,
        request,
        format=None,
    ):
        # Sacamos el audio del request(peticion http) y lo convertimos a archivo, tambien sacamos el id y el ccontexto para la IA
        audio_file = request.FILES["file"]
        id = request.POST.get("id")
        contextJson = request.POST.get("context")
        print("audio_file")
        print(audio_file)
        # guardamos el audio que nos llego por la request
        file_path = os.path.join(settings.MEDIA_ROOT, f"input_{id}")
        with open(file_path, "wb") as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # ***************************************************************************************
        # Creamos una instancia de IAServices
        ia_services = IAServices()

        # ***************************************************************************************
        # Convertimos el audio en texto
        text_convert = ia_services.audio_to_text(file_path=file_path)

        # ***************************************************************************************
        # Enviamos el audio a GPT para que nos responda
        context = json.loads(contextJson)
        # context = list()
        # context.append({
        #     "role": "system",
        #     "content": "Eres un asistente respetuoso"
        # })
        completion = ia_services.gpt_normal(
            text_input=text_convert, context=context, id=id
        )

        # ***************************************************************************************
        # Convertimos la respuesta a Voz
        url_voice_respone = ia_services.text_to_voice(text=completion["text"], id=id)

        # Construye el contenido JSON que es la respuesta
        json_data = {
            "message": "Audio recibido y guardado con éxito",
            "response": completion,
        }

        return JsonResponse(json_data)


def get_audio_response(request, id):
    if request.method == "GET":
        filepath_input = os.path.join(settings.MEDIA_ROOT, f"input_{id}")
        filepath_response = os.path.join(settings.MEDIA_ROOT, f"{id}")

        # Enviamos el audio como respuesta
        audio_file = open(filepath_response, "rb")

        # preparamos la respuesta
        response = HttpResponse(audio_file.read(), content_type="audio/mpeg")
        response["Content-Disposition"] = 'attachment; filename="audio"'

        # Cierra el archivo de audio
        audio_file.close()

        # Eliminamos los archivos de audio creados
        if os.path.exists(filepath_response) and os.path.exists(filepath_input):
            os.remove(filepath_input)
            os.remove(filepath_response)
            print(
                f"El archivo {filepath_response} y {filepath_input} ha sido eliminado exitosamente."
            )
        else:
            print(f"El archivo {filepath_response} o {filepath_input} no existe.")

        return response


def saludar(request):
    return JsonResponse({"message": "saludado"})
