import json
import os

def cargar_datos():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            data = json.load(f)
            data["ejecutando"] = False
            return data
    return{
        "limite_trabajos":15,
        "limite_palabras":50,
        "inicio": 8,
        "fin": 20,
        "aceptados_hoy":0,
        "ejecutando":False
    }


def guardar_datos(config_dict):
    with open("config.json", "w") as f:
        json.dump(config_dict, f, indent=4)