import pandas as pd
import os

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

## CREACION DE TABLA CLIENTES
columnas_datos = ['PRIMER_APELLIDO', 'SEGUNDO_APELLIDO', 'PRIMER_NOMBRE', 
                  'SEGUNDO_NOMBRE', 'FECHA_DE_NACIMIENTO', 'GENERO', 
                  'CELULAR', 'CORREO', 'CIUDAD_REGION', 'PROFESION']
ruta_archivo = f'{CCS.db_tables}/CLIENTES.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'NUMERO_DE_IDENTIFICACION', ruta_archivo, 'CLIENTE_ID')

## CREACION DE TABLA PROFESION
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/PROFESION.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'PROFESION', ruta_archivo, 'PROFESION_ID')

## CREACION DE TABLA MODALIDAD
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/MODALIDAD.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'MODALIDAD', ruta_archivo, 'MODALIDAD_ID')

## CREACION DE TABLA GENERO
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/GENERO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'GENERO', ruta_archivo, 'GENERO_ID')

## CREACION DE TABLA RESPONSABLE_VENTA
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/RESPONSABLE_VENTA.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'RESPONSABLE_VENTA', ruta_archivo, 'RESPONSABLE_VENTA_ID')

## CREACION DE TABLA MEDIO_DE_PAGO
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/MEDIO_DE_PAGO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'MEDIO_DE_PAGO', ruta_archivo, 'MEDIO_DE_PAGO_ID')

## CREACION DE TABLA PROCEDENCIA
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/PROCEDENCIA.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'PROCEDENCIA', ruta_archivo, 'PROCEDENCIA_ID')

## CREACION DE TABLA CURSOS
columnas_datos = ['VALOR_UNITARIO']
ruta_archivo = f'{CCS.db_tables}/CURSO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'CURSO', ruta_archivo, 'CURSO_ID')

## CREACION DE TABLA CIUDAD_REGION
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/CIUDAD_REGION.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'CIUDAD_REGION', ruta_archivo, 'CIUDAD_REGION_ID')

## CREACION DE TABLA CIUDAD_REGION
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/DESCUENTO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'DESCUENTO', ruta_archivo, 'DESCUENTO_ID')

## CREACION DE TABLA DE VENTAS TOTALES ##
def mapear_categorias(df_ventas, df_categorias_lookup, columna_lookup, columna_ventas):
    """
    Reemplaza los valores de una columna de categoría en el DataFrame de ventas
    por el índice (ID) correspondiente de la tabla de categorías.
    Args:
        df_ventas (pd.DataFrame): DataFrame con el registro de ventas.
        df_categorias_lookup (pd.DataFrame): Tabla de referencia con el índice (ID)
                                             y la columna de categorías.
        columna_categoria (str): Nombre de la columna que contiene las categorías 
                                 en df_ventas y df_categorias_lookup.
    Returns:
        pd.DataFrame: DataFrame de ventas con la categoría reemplazada por el ID.
    """
    if not columna_ventas:
        columna_ventas = columna_lookup

    mapa_ids = df_categorias_lookup.set_index(columna_lookup)
    serie_map = mapa_ids[f'{columna_lookup}_ID']
    df_ventas[columna_ventas] = df_ventas[columna_ventas].map(serie_map)
    return df_ventas
#########################################

## CREACION DE TABLA FACT_VENTAS ##
raw_conslidate_df = pd.read_csv(f'{CCS.info_source_path}/consolidate_normalized.csv')
if 'Unnamed: 0' in raw_conslidate_df.columns:
    raw_conslidate_df = raw_conslidate_df.drop('Unnamed: 0', axis=1)

work_colums = ['CIUDAD_REGION', 'CURSO', 'DESCUENTO', 'GENERO', 'MEDIO_DE_PAGO',
               'MODALIDAD', 'PROCEDENCIA', 'PROFESION', 'RESPONSABLE_VENTA', 'ELABORO']

pd.set_option("display.max_columns", None)  # muestra todas las filas
for column_lookup in work_colums:
    print(f'🤖 ID normalizacion para la columna: {column_lookup}')
    table = f'{column_lookup}.xlsx'
    column_ventas = ''
    if column_lookup == 'ELABORO':
        table = 'RESPONSABLE_VENTA.xlsx'
        column_lookup = 'RESPONSABLE_VENTA'
        column_ventas = 'ELABORO'

    df_categorias_lookup = pd.read_excel(f'{CCS.db_tables}/{table}')
    if 'Unnamed: 0' in df_categorias_lookup.columns:
        df_categorias_lookup = df_categorias_lookup.drop('Unnamed: 0', axis=1)
    try:
        raw_conslidate_df = mapear_categorias(
            raw_conslidate_df.copy(),
            df_categorias_lookup.copy(), 
            column_lookup,
            column_ventas
        )
        print("\n🤖✅ Mapeo completado exitosamente.")
        raw_df = raw_conslidate_df[['NUMERO_DE_IDENTIFICACION', 'CURSO', 'MODALIDAD',
       'RENOVACION', 'RESPONSABLE_VENTA', 'FECHA_DE_VENTA', 'VALOR_UNITARIO',
       'DESCUENTO', 'PRECIO_NETO', 'MEDIO_DE_PAGO', 'FECHA_DE_PAGO', 'ELABORO',
       'PROCEDENCIA', 'SEGUIMIENTO_POST-VENTA']]

        raw_df.to_excel(f'{CCS.db_tables}/VENTAS.xlsx', index=True, index_label='VENTA_ID')

    except ValueError as e:
        print(f"\n🤖⚠️ Mapeo fallido: {e}")
#########################################


## CREACION DE TABLA CLIENTES ##
raw_conslidate_df = pd.read_excel(f'{CCS.db_tables}/CLIENTES.xlsx')
if 'Unnamed: 0' in raw_conslidate_df.columns:
    raw_conslidate_df = raw_conslidate_df.drop('Unnamed: 0', axis=1)

work_colums = ['CIUDAD_REGION', 'GENERO', 'PROFESION']

pd.set_option("display.max_columns", None)  # muestra todas las filas
for column_lookup in work_colums:
    print(f'🤖 ID normalizacion para la columna: {column_lookup}')
    table = f'{column_lookup}.xlsx'
    column_ventas = ''

    df_categorias_lookup = pd.read_excel(f'{CCS.db_tables}/{table}')
    if 'Unnamed: 0' in df_categorias_lookup.columns:
        df_categorias_lookup = df_categorias_lookup.drop('Unnamed: 0', axis=1)
    try:
        raw_conslidate_df = mapear_categorias(
            raw_conslidate_df.copy(),
            df_categorias_lookup.copy(), 
            column_lookup,
            column_ventas
        )
        print("\n🤖✅ Mapeo completado exitosamente.")
        raw_conslidate_df.to_excel(f"{CCS.db_tables}/CLIENTES.xlsx", index=False)

    except ValueError as e:
        print(f"\n🤖⚠️ Mapeo fallido: {e}")
#########################################