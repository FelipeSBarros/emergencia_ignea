#! /bin/bash
# acceder a la carpeta del proyecto
# cd emergencia_ignea/
# activa el ambiente virtual
cd /var/www/html/mapas/emergencia/python
source .venv/bin/activate
# ejecuta o request data
rm ../datos/incendios_misiones.geojson
python3 request_data.py
# excluye datos antiguos de prediccion
# ejecuta prediccion
#python3 predict_area.py
# sai do venv
.venv/bin/deactivate
