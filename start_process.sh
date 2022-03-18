#! /bin/bash
# acceder a la carpeta del proyecto
cd emergencia_ignea/
# activa el ambiente virtual
source .venv/bin/activate
# ejecuta o request data
python python/request_data.py
# excluye datos antiguos de prediccion
rm ./datos/incendios_misiones.geojson
# ejecuta prediccion
python python/predict_area.py
# sai do venv
deactivate
echo "fim"
