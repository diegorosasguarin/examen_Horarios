import json
import os

ARCHIVO_HORARIOS = "horarios.json"
ARCHIVO_REPORTE = "reporte_horario.json"

def cargar_horarios():
    """Carga la lista de eventos desde el archivo JSON de persistencia."""
    if not os.path.exists(ARCHIVO_HORARIOS):
        return []
    try:
        with open(ARCHIVO_HORARIOS, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, Exception):
        return []

def guardar_horarios(horarios):
    """Guarda la lista de eventos en el archivo JSON de persistencia."""
    with open(ARCHIVO_HORARIOS, "w", encoding="utf-8") as file:
        json.dump(horarios, file, ensure_ascii=False, indent=4)

def guardar_reporte_json(reporte_datos):
    """Guarda el reporte estructurado en el archivo reporte_horario.json."""
    with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as file:
        json.dump(reporte_datos, file, ensure_ascii=False, indent=4)
