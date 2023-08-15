
# Iniciar Gunicorn con tu aplicación Django
#gunicorn tu_proyecto.wsgi:application --bind 0.0.0.0:$PORT
gunicorn core.wsgi:application 0.0.0.0:$PORT