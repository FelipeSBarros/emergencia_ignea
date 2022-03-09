# Repositorio creado para desarrollo del sistema de apoyo a la mesa de emergecia ignea de Misiones

## Preprando ambiente para desarrollo:

```python
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# Procesamientos nuevos:
El archivo [`request_data.py`](./python/request_data.py) es responsable por ejecutar o request de los datos de incendios, transformarlos en datos espaciales, filtrar aquellos que ocurren en Misiones y guardarlos en geojson.  

# Procesamientos antiguo:
 
1. Ejecuta [script bash](./bash/DatosNASA.sh) para acceder a los datos de incendio de distintos satelites de la NASA e identificar aquellos que están en el [boundingbox](https://en.wikipedia.org/wiki/Minimum_bounding_box) de la provincia de Misiones;  
2. Ejecuta [script js](./js/2nd_step_process.js) para identificar los incendios en la provincia de Misiones;  

# Deploy

[emergenciaignea.herokuapp.com](https://emergenciaignea.herokuapp.com)

```python
heroku run python request_data.py
```