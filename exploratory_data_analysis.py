import numpy as np
import pandas as pd

path = "C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/data_febrero_2024.csv"
data_base = pd.read_csv(path, sep=';')


headListIter = iter(list(data_base.columns))
# first I will find and remove data that hasn't a ID related
id_column = next(headListIter)
data_base = data_base.dropna(subset=id_column)
data_base = data_base[data_base[id_column].apply(lambda x : str(x).strip() !='')]

# I will clean data of 'primer apellido' -> this field must has a value
fst_last_name = next(headListIter)
# I will find if any field is empty
empty = data_base[fst_last_name].apply(lambda x: str(x).strip() == '') | data_base[fst_last_name].isna()

# check if any value si empty
if empty.any():
    print("buscar valor")

print("Continua con los demas")


for head in headListIter:
    print(f'header to update: {head}')






