import numpy as np
import pandas as pd
import os 

### FUNCTION TO GET FILES from the specified directory (need to specify the years) on var years
def get_files():
    files = []
    years = ['2024', '2025']
    for year in years:
        path = f"C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/{year}"
        for file in os.listdir(path):
            if file.endswith('.xlsm'):
                files.append(file)
    return files

### CONSTANTS
main_path = f"C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/"
cleaned_path = f"C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/Cleaned/"
rejected_path = f"C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/Rejected/"

### MAPPING DICTIONARIES
course_prices = {
    'Atención pre-hospitalaria': '$250.000',
    'Duelo': '$80.000',
    'Químicos': '$80.000',
    'Primeros auxilios': '$80.000',
    'Uci': '0',
    'Código verde': '$80.000',
    'Humanización': '$80.000',
    'Clínica de heridas': '$80.000',
    'Citología': '$80.000',
    'Acls': '$300.000',
    'Camillero': '$80.000',
    'Toma de muestras': '$80.000',
    'Bls': '$80.000',
    'Violencia sexual': '$80.000',
    'Pai': '$80.000',
    'Aiepi': '$80.000',
    'Admon de medicamentos': '$80.000',
    'Ove': '$80.000',
    'Iami': '$80.000',
    'Donante': '$80.000',
    'Violencia de género': '$80.000',
    'Igualdad de género': '$80.000',
    'Brigada': '$80.000',
    'Paliativos': '$80.000',
    'Poct': '$80.000',
    'Implante': '$80.000',
    'Salud mental': '$80.000',
    'Primeros auxilios p': '$80.000',
    'Conflicto armado': '$80.000',
    'Manipulación de alimentos': '$80.000',
    'Discapacidad': '$80.000',
    'Adulto mayor': '$80.000',
    'Manejo defensivo': '$80.000',
    'Aclsn': '$80.000',
    'Paciente': '$80.000',
    'Residuos': '$80.000'
}

