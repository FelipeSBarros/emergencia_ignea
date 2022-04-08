#! /bin/bash
# acceder a la carpeta del proyecto
cd emergencia_ignea/
# activa el ambiente virtual
source .venv/bin/activate
# ejecuta o request data
python3 python/request_data.py
# ejecuta prediccion
python3 python/predict_area.py
# sai do venv
deactivate
echo "fim"
