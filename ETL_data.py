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

def re_organize_columns(df):
    n_df = pd.DataFrame()
    columns = df.columns.tolist()
    provided_order = [
    ['NUMERO DE IDENTIFICACION'],
    ['PRIMER APELLIDO'],
    ['SEGUNDO APELLIDO'],
    ['PRIMER NOMBRE'],
    ['SEGUNDO NOMBRE'],
    ['FECHA DE NACIMIENTO'],
    ['GENERO'],
    ['CELULAR'],
    ['CORREO'],
    ['CIUDAD/REGION'],
    ['PROFESION', 'PERFIL DEL PROFESIONAL'],
    ['CURSO'],
    ['MODALIDAD'],
    ['RENOVACION'],
    ['RESPONSABLE VENTA', 'RESPONSABLE'],
    ['FECHA DE VENTA'],
    ['VALOR UNITARIO'],
    ['DESCUENTO'],
    ['PRECIO NETO'],
    ['MEDIO DE PAGO'],
    ['FECHA DE PAGO'],
    ['ELABORO', 'REALIZADOR'],
    ['PROCEDENCIA'],
    ['SEGUIMIENTO POST-VENTA']
]

    rejected_col = ['DIA', 'MES', 'NOMBRE CURSO', 'NOMBRE COMPLETO', 'NOMBRE CERTIFICADO', 'NOMBRE PDF']
    New_colums = ['CORREO', 'CIUDAD/REGION', 'MODALIDAD', 'RENOVACION', 'FECHA DE VENTA', 'DESCUENTO', 'PRECIO NETO','PROCEDENCIA','SEGUIMIENTO POST-VENTA']
    
    for i, col in enumerate(provided_order, start=0):
        for item in col:
            print("Aqui ITEM: ", item)
            if item in columns:
                values = df.pop(item)
                print(item, values.head(2))
                n_df.insert(i, col[0], values)
                break
            elif item in New_colums:
                n_df.insert(i, col[0], 'null')
                break
            else:
                print('No encontro')
                pass
    
    return n_df

data_base = re_organize_columns(data_base)
print(data_base['CORREO'].head())


### START DATA CLEANING LOGIC ###
headListIter = iter(list(data_base.columns))

# 'NUMERO DE IDENTIFICACION' FIELD
id_column = next(headListIter)
data_base[id_column] = data_base[id_column].astype('str').apply(lambda num : clean_numer(num))
data_base = data_base.dropna(subset=id_column)
data_base = data_base[data_base[id_column].apply(lambda x : str(x).strip() !='')]

# 'PRIMER APELLIDO' FIELD
fst_last_name = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, fst_last_name, id_column, ['R','C','D'])

# 'SEGUNDO APELLIDO' FIELD
scd_last_name = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_last_name, id_column, ['R','C','F'])

# 'PRIMER NOMBRE' FIELD
fst_name = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, fst_name, id_column, ['R','C','D'])

# 'SEGUNDO NOMBRE' FIELD
scd_name = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_name, id_column, ['R','C','F'])

# 'FECHA DE NACIMIENTO' FIELD
brn_date = next(headListIter)
data_base[brn_date] = pd.to_datetime(data_base[brn_date], errors='coerce')
data_base, wrong_df = check_if_empty(wrong_df, data_base, brn_date, id_column, ['R'])
data_base[brn_date] = data_base[brn_date].fillna(pd.Timestamp('01/01/1900'))  # Fill with a default date if NaT
data_base[brn_date] = data_base[brn_date].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

# 'GENERO' FIELD
gender = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, gender, id_column, ['R','F'])
replace_text(data_base, gender, gender_sre)

# 'CELULAR' FIELD
phone = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, phone, id_column, ['R','F'])

# 'CORREO' new column added on data frame
mail = next(headListIter)
data_base[mail].fillna('null', inplace=True)

# 'CIUDAD/REGION' new column added on data frame
city = next(headListIter)
if (data_base[city]=='null').all():
    data_base[city] = 'Pasto - Nariño'  # Default value if all are NaN
else:
    data_base[city].fillna('Pasto - Nariño', inplace=True)

# 'PROFESION' FIELD
profession = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, profession, id_column, ['R','C','F'])

# 'CURSO' FIELD
course = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, course, id_column, ['C','D'])

# 'MODALIDAD' FIELD
modality = next(headListIter)
if (data_base[modality]=='null').all():
    data_base[modality] = 'Virtual asincrónica'
else:
    data_base, wrong_df = check_if_empty(wrong_df, data_base, modality, id_column, ['R','C','F'])

# 'RENOVACION' new column added on data frame
renew = next(headListIter)
if (data_base[renew]=='null').all():
    data_base[renew] = 'No'
else:
    data_base, wrong_df = check_if_empty(wrong_df, data_base, renew, id_column, ['R','C','F'])

# 'RESPONSABLE VENTA' FIELD
seller = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, seller, id_column, ['R','T','F'])

# 'FECHA DE VENTA' new column added on data frame
sale_date = next(headListIter)
pay_date = 'FECHA DE PAGO'  # Assuming this is the same as the next field
if (data_base[sale_date]=='null').all():
    data_base[sale_date] = data_base[pay_date]  # Default to pay_date if all are NaN
else:
    data_base, wrong_df = check_if_empty(wrong_df, data_base, sale_date, id_column, ['R'])
data_base[sale_date] = pd.to_datetime(data_base[sale_date], errors='coerce')
data_base[sale_date] = data_base[sale_date].fillna(pd.Timestamp('01/01/1900'))
data_base[sale_date] = data_base[sale_date].apply(lambda x : x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

# 'VALOR UNITARIO' FIELD
unit_value = next(headListIter)
data_base[unit_value] = pd.to_numeric(data_base[unit_value], errors='coerce')
data_base, wrong_df = check_if_empty(wrong_df, data_base, unit_value, course, ['R'])

# 'DESCUENTO' new column added on data frame
discount = next(headListIter)
if (data_base[discount]=='null').all():
    data_base[discount] = 'Sin descuento'
else:
    data_base, wrong_df = check_if_empty(wrong_df, data_base, discount, id_column, ['R','C','F'])

# 'PRECIO NETO' new column added on data frame
net_price = next(headListIter)
if (data_base[net_price]=='null').all():
    data_base[net_price] = data_base[unit_value]
else:
    data_base[unit_value] = pd.to_numeric(data_base[unit_value], errors='coerce')
    data_base, wrong_df = check_if_empty(wrong_df, data_base, net_price, id_column, ['R'])

# 'MEDIO DE PAGO' FIELD
payment = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, payment, id_column, ['R','T','F'])

# 'FECHA DE PAGO' FIELD
pay_date = next(headListIter)
data_base[pay_date] = pd.to_datetime(data_base[pay_date], errors='coerce')
ata_base, wrong_df = check_if_empty(wrong_df, data_base, pay_date, id_column, ['R'])
data_base[pay_date] = data_base[pay_date].fillna(pd.Timestamp('01/01/1900'))
data_base[pay_date] = data_base[pay_date].apply(lambda x : x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

# 'ELABORO' FIELD
maker = next(headListIter)
data_base, wrong_df = check_if_empty(wrong_df, data_base, maker, id_column, ['R','T','F'])

# 'PROCEDENCIA' new column added on data frame
origin = next(headListIter)
if (data_base[origin]=='null').all():
    data_base[origin] = 'Facebook'
else:
    data_base, wrong_df = check_if_empty(wrong_df, data_base, origin, id_column, ['R','C','F'])

# 'SEGUIMIENTO POST-VENTA' new column added on data frame
follow_up = next(headListIter)
if (data_base[follow_up]=='null').all():
    data_base[follow_up] = 'null'
else:
    data_base, wrong_df = check_if_empty(wrong_df, data_base, follow_up, id_column, ['C','F'])


###### VISUALITZATION OF DATA CLEANING RESULTS ######

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
