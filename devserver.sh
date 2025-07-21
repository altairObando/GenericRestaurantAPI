#!/bin/bash

# Obtener la dirección IP local de la interfaz en1 (Wi-Fi)
IP_LOCAL=$(ipconfig getifaddr en1)
PORT=8000

echo "--- Iniciando Servidor Django ---"
echo "Servidor accesible en: http://${IP_LOCAL}:${PORT}/"
echo "Presiona Ctrl+C para detener el servidor."
echo "---------------------------------"

# Activar el entorno virtual (aunque no lo veas reflejado en el shell principal,
# este comando intentará activarlo para la ejecución de la siguiente línea)
source env/bin/activate
# Instalar paquetes
pip install --upgrade pip
pip install -r requirements.txt
# Ejecutar el servidor Django
# Usa 0.0.0.0 para que sea accesible desde otras máquinas en tu red local.
python manage.py runserver 0.0.0.0:${PORT}
