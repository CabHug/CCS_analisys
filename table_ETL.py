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
df_result.to_excel(f'{CCS.db_tables}/CURSOS.xlsx', index=True, index_label="CURSO_ID")
print(df_result)
print("*"*50)

df_result = pd.DataFrame({'CIUDAD/REGION': raw_consl_df['CIUDAD/REGION'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/CIUDAD_REGION.xlsx', index=True, index_label="CIUDAD/REGION_ID")
print(df_result)
print("*"*50)

df_result = pd.DataFrame({'PROFESION': raw_consl_df['PROFESION'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/PROFESION.xlsx', index=True, index_label="PROFESION_ID")
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'MODALIDAD': raw_consl_df['MODALIDAD'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/MODALIDAD.xlsx', index=True, index_label="MODALIDAD_ID")
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'GENERO': raw_consl_df['GENERO'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/GENERO.xlsx', index=True, index_label="GENERO_ID")
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'RESPONSABLE_VENTA': raw_consl_df['RESPONSABLE_VENTA'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/RESPONSABLE_VENTA.xlsx', index=True, index_label="RESPONSABLE_VENTA_ID")
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'MEDIO_DE_PAGO': raw_consl_df['MEDIO_DE_PAGO'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/MEDIO_DE_PAGO.xlsx', index=True, index_label="MEDIO_DE_PAGO_ID")
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'PROCEDENCIA': raw_consl_df['PROCEDENCIA'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/PROCEDENCIA.xlsx', index=True, index_label="PROCEDENCIA_ID")
print(df_result)
print("*" * 50)

df_result = pd.DataFrame({'DESCUENTO': raw_consl_df['DESCUENTO'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/DESCUENTO.xlsx', index=True, index_label="DESCUENTO_ID")
print(df_result)
print("*" * 50)