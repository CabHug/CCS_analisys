import numpy as np
import pandas as pd

from functions import *
from data_source.df_source import main_path
from data_source.df_source import cleaned_path
from data_source.df_source import rejected_path
from data_source.df_source import gender_sre

### READ DATA FROM RAW FILES
data_base = pd.read_excel(main_path)

### CREATE A NEW DATA FRAME TO STORE WRONG DATA
wrong_df = pd.DataFrame(columns=data_base.columns)

### STEPS BEFORE DATA CLEANING
# Cleaning headers of hidden spaces
data_base.columns = data_base.columns.str.strip()
# Remove the first row from each data frame (docuemnt's index column)
data_base.drop(data_base.columns[0], axis=1, inplace=True)


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
data_base = move_column(data_base, 14, 'ELABORO')
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
data_base[id_column] = data_base[id_column].astype('str').apply(lambda num : clean_numer(num))
data_base = data_base.dropna(subset=id_column)
data_base = data_base[data_base[id_column].apply(lambda x : str(x).strip() !='')]

# 'PRIMER APELLIDO' FIELD
# I will clean data of 'primer apellido' -> this field must has a value
fst_last_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id
data_base, wrong_df = check_if_empty(wrong_df, data_base, fst_last_name, id_column, ['R','D'])

# 'SEGUNDO APELLIDO' FIELD
# I will clean data of 'segundo apellido' -> this field can has null values
scd_last_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id if not will fill the filed with null
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_last_name, id_column, ['R','C','F'])

# 'PRIMER NOMBRE' FIELD
# I will clean data of 'Primer nombre' -> this field must has a value
fst_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id
data_base, wrong_df = check_if_empty(wrong_df, data_base, fst_name, id_column, ['R','D'])

# 'SEGUNDO NOMBRE' FIELD
# I will clean data of 'segundo nombre' -> this field can has null values
scd_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id if not will fill the filed with null
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_name, id_column, ['R','C','F'])

# 'FECHA DE NACIMIENTO' FIELD
# I will clean data of 'fecha de nacimiento' -> this field can has null values
brn_date = next(headListIter)
data_base[brn_date] = pd.to_datetime(data_base[brn_date], errors='coerce')
data_base, wrong_df = check_if_empty(wrong_df, data_base, brn_date, id_column, ['R'])
data_base[brn_date] = data_base[brn_date].fillna(pd.Timestamp('01/01/1900'))  # Fill with a default date if NaT
data_base[brn_date] = data_base[brn_date].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

# 'GENERO' FIELD
# I will clean data of 'fecha de nacimiento' -> this field can has null values
gender = next(headListIter)
# I will look for rows with same id and the needed info
data_base, wrong_df = check_if_empty(wrong_df, data_base, gender, id_column, ['R','F'])
replace_text(data_base, gender, gender_sre)

# 'CELULAR' FIELD
# I will clean data of 'Celular' -> this field can has null values
phone = next(headListIter)
#data_base[phone] = data_base[phone].astype('str').apply(lambda num: phone_validation(num, codigo='CO'))
data_base, wrong_df = check_if_empty(wrong_df, data_base, phone, id_column, ['R','F'])

# 'PROFESION' FIELD
# I will clean data of 'Profesion' -> this field can has null values
profession = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, profession, id_column, ['R','C','F'])

# 'CURSO' FIELD
course = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, course, id_column, ['C','D'])

# 'RESPONSABLE VENTA' FIELD
seller = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, seller, id_column, ['R','T','F'])

# 'VALOR UNITARIO' FIELD
unit_value = next(headListIter)
data_base[unit_value] = pd.to_numeric(data_base[unit_value], errors='coerce')
data_base, wrong_df = check_if_empty(wrong_df, data_base, unit_value, course, ['R'])

# 'MEDIO DE PAGO' FIELD
payment = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, payment, id_column, ['R','T','F'])

# 'FECHA DE PAGO' FIELD
pay_date = next(headListIter)
data_base[pay_date] = pd.to_datetime(data_base[pay_date], errors='coerce')
ata_base, wrong_df = check_if_empty(wrong_df, data_base, pay_date, id_column, ['R'])
data_base[pay_date] = data_base[pay_date].fillna(pd.Timestamp('01/01/1900'))
data_base[pay_date] = data_base[pay_date].apply(lambda x : x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

# 'ELAVORO' FIELD
maker = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, maker, id_column, ['R','T','F'])

## I'LL AGREGATE MISSING COLUMS TO THE DATAFRAME

# 'CORREO' new column added on data frame
mail = 'COREO'
data_base.insert(9, mail, 'null')

# 'CIUDAD/REGION' new column added on data frame
city = 'CIUDAD/REGION'
data_base.insert(10, city, 'Pasto - Nariño')

# 'MODALIDAD' new column added on data frame
modality = 'MODALIDAD'
data_base.insert(13, modality, 'Virtual asincrónica')

# 'RENOVACION' new column added on data frame
renew = 'RENOVACION'
data_base.insert(14, renew, 'No')

# 'FECHA DE VENTA' new column added on data frame
sale_date = 'FECHA DE VENTA'
data_base.insert(16, sale_date, data_base[pay_date])

# 'DESCUENTO' new column added on data frame
discount = 'DESCUENTO'
data_base.insert(18, discount, 'Sin descuento')

# 'PRECIO NETO' new column added on data frame
net_price = 'PRECIO NETO'
data_base.insert(19, net_price, data_base[unit_value])

# 'PROCEDENCIA' new column added on data frame
origin = 'PROCEDENCIA'
data_base.insert(22, origin, 'WhatsApp')

# 'SEGUIMIENTO POST-VENTA' new column added on data frame
follow_up = 'SEGUIMIENTO POST-VENTA'
data_base.insert(23, follow_up, 'null')


print('-'*50)
print(data_base.isna().sum())
print('-'*50)
print(wrong_df)
print('-'*50)
print('Detalles del data frame')
print('-'*50)
print(data_base.dtypes)




print('Archivo guardado!')
data_base.to_excel(cleaned_path, index=False, engine="openpyxl")
wrong_df.to_excel(rejected_path, index=False, engine="openpyxl")
print('Archivo de datos erróneos guardado!')


