import numpy as np
import pandas as pd

# READ DATA FROM RAW FILES
path = "C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/CCS_FEBRERO_2024.xlsm"
data_base = pd.read_excel(path)

# CREATE A NEW DATA FRAME TO STORE WRONG DATA
wrong_df = pd.DataFrame(columns=data_base.columns)

# STEPS BEFORE DATA CLEANING
# Cleaning headers of hidden spaces
data_base.columns = data_base.columns.str.strip()
# Remove the first row from each data frame (docuemnt's index column)
data_base.drop(data_base.columns[0], axis=1, inplace=True)

# FUNCTION DEFINITION
def find_replace_value(i, id, df, id_column, column):
    value = df.loc[df[id_column] == id, column].dropna().iloc[0]
    df.loc[i, column] = value

# function to find missing information in dataframe, find if any similar data exist to replace in missing one
# parameter action [R(Raplace with similar values), D(drop missing values), F(fill missing values with null)]
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
                #value = df.loc[df[id_column] == id, column].dropna().iloc[0]
                #df.loc[i, column] = value
            print("Row that has value: \n", has_value)

        elif action == 'D':

            for i, id in has_no_val.items():
                wdf = pd.concat([wdf, df.loc[[i]]], ignore_index=True)
                df = df.drop(i, axis=0)
            print("Row that hasn't value: \n", has_no_val)

        # Option when whan to perform data filling with null value you can customice it
        elif action == 'F':
            filling = 'null'
            if not has_value.empty:
                print('Please perform a replacement!')
            
            for i, id in has_no_val.items():
                df.loc[i, column] = filling

        else:
            print("Error! action parameter wrong.")

    return df, wdf
    

# START DATA CLEANING LOGIC
headListIter = iter(list(data_base.columns))

# first I will find and remove data that hasn't a ID related
id_column = next(headListIter)
data_base = data_base.dropna(subset=id_column)
data_base = data_base[data_base[id_column].apply(lambda x : str(x).strip() !='')]

# I will clean data of 'primer apellido' -> this field must has a value
fst_last_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id
data_base, wrong_df = check_if_empty(wrong_df, data_base, fst_last_name, ['R','D'])

# I will clean data of 'primer apellido' -> this field must has a value
scd_last_name = next(headListIter)
# I will find if any field is empty and fill it with similar data getting from another field with tha same customer_id
data_base, wrong_df = check_if_empty(wrong_df, data_base, scd_last_name, 'F')

#for head in headListIter:
#    print(f'header to update: {head}')


print('-'*50)
print(data_base.isna().sum())
print('-'*50)
print(wrong_df)


print('Archivo guardado!')
data_base.to_excel("C:/Users/Hugo/Documents/MEGA/PROYECTOS/CCS/Analisis CCS/Python-analisys/data_source/CCS_FEBRERO_2024_cleaned.xlsx", index=False, engine="openpyxl")



