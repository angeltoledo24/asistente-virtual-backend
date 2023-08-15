from django.urls import path, include
from rest_framework import routers
from . import views
from .views import AudioUploadView, get_audio_response



urlpatterns = [
    path('chat/voice', AudioUploadView.as_view(), name='voiceToText'),
    path("chat/audio/<str:id>", get_audio_response, name="audioResponse")
    # Otras rutas...
]
