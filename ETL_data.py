import numpy as np
import pandas as pd

import phonenumbers

from data_source.df_source import gender_sre

### READ DATA FROM RAW FILES
path = "C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/CCS_FEBRERO_2024.xlsm"
data_base = pd.read_excel(path)

### CREATE A NEW DATA FRAME TO STORE WRONG DATA
wrong_df = pd.DataFrame(columns=data_base.columns)

### STEPS BEFORE DATA CLEANING
# Cleaning headers of hidden spaces
data_base.columns = data_base.columns.str.strip()
# Remove the first row from each data frame (docuemnt's index column)
data_base.drop(data_base.columns[0], axis=1, inplace=True)

### FUNCTION DEFINITION
def find_replace_value(i, id, df, id_column, column):
    value = df.loc[df[id_column] == id, column].dropna().iloc[0]
    df.loc[i, column] = value

# function to find missing information in dataframe, find if any similar data exist to replace in missing one
# parameter action [R(Raplace with similar values), D(drop missing values), F(fill missing values with null), C(To capitalize the text)]
def check_if_empty(wdf, df, column, actions):
    print('*'*50)
    print(f'Data cleaning for {column} column')
    id_column = 'NUMERO DE IDENTIFICACION'
    # This mask will return al serie bool with values that being empty or NAN
    mask = df[column].apply(lambda x: str(x).strip() == '') | df[column].isna()
    # This serie will contain boolean values, when True has missing data
    id_invalid = df.loc[mask, id_column]
    # This serie will cntain boolean values, when True has valid data
    id_valid = df.loc[~mask, id_column]
    # This serie will contain values that has a values despite has missing values in another row
    has_value = id_invalid[id_invalid.isin(id_valid)]
    # This serie will contain values that hasn't a value despite has missing values in another row
    has_no_val = id_invalid[~id_invalid.isin(id_valid)]

    for action in  actions:
        # Option when whant to perform replacement with backup
        if action == 'R':
            for i, id in has_value.items():
                find_replace_value(i, id, df, id_column, column)
            print("Row that has value: \n", has_value)

        # Option when whant to drop a invalid value
        elif action == 'D':
            for i, id in has_no_val.items():
                wdf = pd.concat([wdf, df.loc[[i]]], ignore_index=True)
                df = df.drop(i, axis=0)
                df = df.reset_index()
            print("Row that hasn't value: \n", has_no_val)

        # Option when whan to perform data filling with null value you can customice it
        elif action == 'F':
            filling = 'null'
            if not has_value.empty:
                print('Please perform a replacement!')
            
            for i, id in has_no_val.items():
                df.loc[i, column] = filling

        # Option to capitalice the text
        elif action == 'C':
            df[column] = df[column].str.capitalize()


        else:
            print("Error! action parameter wrong.")

    return df, wdf

def move_column(df, index, name, n_name=None):
    if n_name is None:
        n_name = name
    values = df.pop(name)
    df.insert(index, n_name, values)

    return df

def remove_column(df, name):
    df.drop(name, axis=1, inplace=True)

def replace_text(df, column, sre):
    df[column] = df[column].map(sre).fillna('null')

def phone_validation(number, codigo='CO'):
    try:
        telefono_v = phonenumbers.parse(number, codigo)
        if phonenumbers.is_valid_number(telefono_v):
            return number
        else:
            return 'null'
    except phonenumbers.NumberParseException:
        return 'null'


### MOVING COLUMNS AND DROPPING COLUMNS
data_base = move_column(data_base, 5, 'FECHA DE NACIMIENTO')
data_base = move_column(data_base, 6, 'GENERO')
data_base = move_column(data_base, 7, 'CELULAR')
data_base = move_column(data_base, 8, 'PERFIL DEL PROFESIONAL', 'PROFESION')
data_base = move_column(data_base, 9, 'CURSO')
data_base = move_column(data_base, 10, 'RESPONSABLE', 'RESPONSABLE VENTA')
data_base = move_column(data_base, 11, 'VALOR UNITARIO')
data_base = move_column(data_base, 12, 'MEDIO DE PAGO')
data_base = move_column(data_base, 13, 'FECHA DE PAGO')
data_base = move_column(data_base, 14, 'REALIZADOR', 'ELABORO')
remove_column(data_base, 'DIA')
remove_column(data_base, 'MES')
remove_column(data_base, 'NOMBRE CURSO')
remove_column(data_base, 'NOMBRE COMPLETO')
remove_column(data_base, 'NOMBRE CERTIFICADO')
remove_column(data_base, 'NOMBRE PDF')


### START DATA CLEANING LOGIC ###
headListIter = iter(list(data_base.columns))
# 'NUMERO DE IDENTIFICACION' FIELD
# first I will find and remove data that hasn't a ID related
id_column = next(headListIter)
data_base = data_base.dropna(subset=id_column)
data_base = data_base[data_base[id_column].apply(lambda x : str(x).strip() !='')]

# 'PRIMER APELLIDO' FIELD
# I will clean data of 'primer apellido' -> this field must has a value
fst_last_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id
data_base, wrong_df = check_if_empty(wrong_df, data_base, fst_last_name, ['R','D'])

# 'SEGUNDO APELLIDO' FIELD
# I will clean data of 'segundo apellido' -> this field can has null values
scd_last_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id if not will fill the filed with null
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_last_name, ['R','F'])

# 'PRIMER NOMBRE' FIELD
# I will clean data of 'Primer nombre' -> this field must has a value
fst_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id
data_base, wrong_df = check_if_empty(wrong_df, data_base, fst_name, ['R','D'])

# 'SEGUNDO NOMBRE' FIELD
# I will clean data of 'segundo nombre' -> this field can has null values
scd_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id if not will fill the filed with null
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_name, ['R','F'])

# 'FECHA DE NACIMIENTO' FIELD
# I will clean data of 'fecha de nacimiento' -> this field can has null values
brn_date = next(headListIter)

# 'GENERO' FIELD
# I will clean data of 'fecha de nacimiento' -> this field can has null values
gender = next(headListIter)
# I will look for rows with same id and the needed info
data_base, wrong_df = check_if_empty(wrong_df, data_base, gender, ['R','F'])
replace_text(data_base, gender, gender_sre)

# 'CELULAR' FIELD
# I will clean data of 'Celular' -> this field can has null values
phone = next(headListIter)
data_base[phone] = data_base[phone].astype('str').apply(lambda num: phone_validation(num, codigo='CO'))

# 'PROFESION' FIELD
# I will clean data of 'Profesion' -> this field can has null values
profession = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_last_name, ['R','F'])




print('-'*50)
print(data_base.isna().sum())
print('-'*50)
print(wrong_df)


print('Archivo guardado!')
data_base.to_excel("C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/CCS_FEBRERO_2024_cleaned.xlsx", index=False, engine="openpyxl")



