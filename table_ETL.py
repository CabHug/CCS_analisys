import pandas as pd

from OOP_classes import *

CCS = Project()
# Strating with CCS object configuration
CCS.set_current_year() # Set current year in object attributes
CCS.read_config_json() # Set paths required for Extract data files
CCS.find_work_foldes() # Set work folders inside data_source folder
CCS.set_work_files_per_year() # Create a dictionario with work files per year

raw_consl_df = pd.read_csv(f'{CCS.info_source_path}/consolidate_normalized.csv')

# TABLE STRUCTURE CREATION
print("*"*50)
print("## ​​​🤖​ TABLE STRUCTURE CREATION ​​​🤖​ ##")
print("*"*50)

df_result = raw_consl_df.groupby('CURSO', as_index=False)['VALOR_UNITARIO'].first()
print(df_result)

print("*"*50)

df_result = pd.DataFrame({'CIUDAD/REGION': raw_consl_df['CIUDAD/REGION'].unique()}).sort_index()
print(df_result)
print("*"*50)

df_result = pd.DataFrame({'PROFESION': raw_consl_df['PROFESION'].unique()}).sort_index()
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'MODALIDAD': raw_consl_df['MODALIDAD'].unique()}).sort_index()
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'GENERO': raw_consl_df['GENERO'].unique()}).sort_index()
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'RESPONSABLE_VENTA': raw_consl_df['RESPONSABLE_VENTA'].unique()}).sort_index()
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'MEDIO_DE_PAGO': raw_consl_df['MEDIO_DE_PAGO'].unique()}).sort_index()
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'PROCEDENCIA': raw_consl_df['PROCEDENCIA'].unique()}).sort_index()
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'DESCUENTO': raw_consl_df['DESCUENTO'].unique()}).sort_index()
print(df_result)
print("*" * 50)