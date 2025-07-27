import numpy as np
import pandas as pd

path = "C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/CCS_FEBRERO_2024.xlsm"
data_base = pd.read_excel(path)

# Cleaning headers of hidden spaces
data_base.columns = data_base.columns.str.strip()

def check_if_empty(df, column, ):
    id_column = 'NUMERO DE IDENTIFICACION'
    # This will return al serie bool with values that being empty or NAN
    mask = df[column].apply(lambda x: str(x).strip() == '') | df[column].isna()
    id_invalid = df.loc[mask, id_column]

    # Look for for another register with the same Id that has the missing info
    id_valid = df.loc[~mask, id_column]
    repeated_id = id_invalid[id_invalid.isin(id_valid)]
    is_not = id_invalid[~id_invalid.isin(id_valid)]
    return is_not


headListIter = iter(list(data_base.columns))
# first I will find and remove data that hasn't a ID related
id_column = next(headListIter)
data_base = data_base.dropna(subset=id_column)
data_base = data_base[data_base[id_column].apply(lambda x : str(x).strip() !='')]

# I will clean data of 'primer apellido' -> this field must has a value
fst_last_name = next(headListIter)
# I will find if any field is empty
index = check_if_empty(data_base, fst_last_name)
print(index)

for head in headListIter:
    print(f'header to update: {head}')






