import pandas as pd
import os

from OOP_classes import *

CCS = Project()
# Strating with CCS object configuration
CCS.set_current_year() # Set current year in object attributes
CCS.read_config_json() # Set paths required for Extract data files
CCS.find_work_foldes() # Set work folders inside data_source folder
CCS.set_work_files_per_year() # Create a dictionario with work files per year

consl_df = pd.read_csv(f'{CCS.info_source_path}/consolidate_normalized.csv')
raw_consl_df = consl_df.copy()

# TABLE STRUCTURE CREATION
print("*"*50)
print("## ​​​🤖​ TABLE STRUCTURE CREATION ​​​🤖​ ##")
print("*"*50)

## CREACION DE TABLA CLIENTES
columnas_datos = ['PRIMER_APELLIDO', 'SEGUNDO_APELLIDO', 'PRIMER_NOMBRE', 
                  'SEGUNDO_NOMBRE', 'FECHA_DE_NACIMIENTO', 'GENERO', 
                  'CELULAR', 'CORREO', 'CIUDAD_REGION', 'PROFESION']
ruta_archivo = f'{CCS.db_tables}/a_base/CLIENTES.xlsx'
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


def mapear_categorias_corregida(df_ventas: pd.DataFrame, 
                                df_categorias_lookup: pd.DataFrame, 
                                columna_categoria: str, # Columna de categoría (el valor que coincide)
                                columna_id: str,        # Columna que contiene el ID (el valor que reemplaza)
                                columna_a_modificar: str = None # Columna en df_ventas a la que aplicar el mapeo
                               ) -> pd.DataFrame:
    """
    Reemplaza los valores de una columna en df_ventas por el ID
    correspondiente de df_categorias_lookup.
    """
    
    # Si no se especifica la columna a modificar en df_ventas, se asume que
    # es la misma columna de categorías (comportamiento habitual).
    if columna_a_modificar is None:
        columna_a_modificar = columna_categoria

    # 1. Crear el mapa de Series: Categoría -> ID
    # Aquí es donde se establece que la categoría es el índice (la clave de búsqueda)
    # y el ID es el valor que queremos obtener.
    mapa_ids_serie = df_categorias_lookup.set_index(columna_categoria)[columna_id]
    
    # 2. Aplicar el mapeo a la columna de ventas
    df_ventas[columna_a_modificar] = df_ventas[columna_a_modificar].map(mapa_ids_serie)
    
    return df_ventas

## CREACION DE TABLA CLIENTES ##
raw_conslidate_df = pd.read_excel(f'{CCS.db_tables}/a_base/CLIENTES.xlsx')
if 'Unnamed: 0' in raw_conslidate_df.columns:
    raw_conslidate_df = raw_conslidate_df.drop('Unnamed: 0', axis=1)

work_colums = ['CIUDAD_REGION', 'GENERO', 'PROFESION']

pd.set_option("display.max_columns", None)  # muestra todas las filas
for column_lookup in work_colums:
    print(f'🤖 ID normalizacion para la columna: {column_lookup}')
    table = f'{column_lookup}.xlsx'
    column_lookup_id = f'{column_lookup}_ID'
    column_ventas = None

    df_categorias_lookup = pd.read_excel(f'{CCS.db_tables}/{table}')
    if 'Unnamed: 0' in df_categorias_lookup.columns:
        df_categorias_lookup = df_categorias_lookup.drop('Unnamed: 0', axis=1)
    try:
        raw_conslidate_df = mapear_categorias_corregida(
            raw_conslidate_df.copy(),
            df_categorias_lookup.copy(), 
            column_lookup,
            column_lookup_id,
            column_ventas
        )
        print("\n🤖✅ Mapeo completado exitosamente.")
        raw_df = raw_conslidate_df.copy()
        raw_df.rename(columns={
            'CIUDAD_REGION': 'CIUDAD_REGION_ID',
            'GENERO': 'GENERO_ID',
            'PROFESION': 'PROFESION_ID'
        }, inplace=True)
        raw_df.to_excel(f"{CCS.db_tables}/CLIENTES.xlsx", index=False)

    except ValueError as e:
        print(f"\n🤖⚠️ Mapeo fallido: {e}")
""" 

"""
#########################################

## CREACION DE TABLA FACT_VENTAS ##
raw_conslidate_df = consl_df.copy()
if 'Unnamed: 0' in raw_conslidate_df.columns:
    raw_conslidate_df = raw_conslidate_df.drop('Unnamed: 0', axis=1)

work_colums = ['NUMERO_DE_IDENTIFICACION', 'CURSO', 'DESCUENTO', 'MEDIO_DE_PAGO', 'MODALIDAD',
               'PROCEDENCIA', 'RESPONSABLE_VENTA', 'ELABORO']

pd.set_option("display.max_columns", None)  # muestra todas las filas
for column_lookup in work_colums:
    print(f'🤖 ID normalizacion para la columna: {column_lookup}')
    table = f'{column_lookup}.xlsx'
    column_lookup_id = f'{column_lookup}_ID'
    column_ventas = None
    if column_lookup == 'ELABORO':
        table = 'RESPONSABLE_VENTA.xlsx'
        column_lookup = 'RESPONSABLE_VENTA'
        column_ventas = 'ELABORO'
        column_lookup_id = 'RESPONSABLE_VENTA_ID'

    elif column_lookup == 'NUMERO_DE_IDENTIFICACION':
        table = 'CLIENTES.xlsx'
        column_lookup = 'NUMERO_DE_IDENTIFICACION'
        column_ventas = 'NUMERO_DE_IDENTIFICACION'
        column_lookup_id = 'CLIENTE_ID'

    df_categorias_lookup = pd.read_excel(f'{CCS.db_tables}/{table}')
    if 'Unnamed: 0' in df_categorias_lookup.columns:
        df_categorias_lookup = df_categorias_lookup.drop('Unnamed: 0', axis=1)
    try:
        raw_conslidate_df = mapear_categorias_corregida(
            raw_conslidate_df.copy(),
            df_categorias_lookup.copy(), 
            column_lookup,
            column_lookup_id,
            column_ventas
        )
        print("\n🤖✅ Mapeo completado exitosamente.")
        raw_df = raw_conslidate_df[['NUMERO_DE_IDENTIFICACION', 'CURSO', 'MODALIDAD',
        'RENOVACION', 'RESPONSABLE_VENTA', 'FECHA_DE_VENTA', 'DESCUENTO', 
        'PRECIO_NETO', 'MEDIO_DE_PAGO', 'FECHA_DE_PAGO', 'ELABORO',
        'PROCEDENCIA', 'SEGUIMIENTO_POST-VENTA']]

        raw_df.to_excel(f'{CCS.db_tables}/a_base/VENTAS.xlsx', index=True, index_label='VENTA_ID')
    except ValueError as e:
        print(f"\n🤖⚠️ Mapeo fallido: {e}")


normal_raw_df = pd.read_excel(f'{CCS.db_tables}/a_base/VENTAS.xlsx')
normal_raw_df.rename(columns={
        'NUMERO_DE_IDENTIFICACION': 'CLIENTE_ID',
        'CURSO': 'CURSO_ID',
        'MODALIDAD': 'MODALIDAD_ID',
        'RESPONSABLE_VENTA': 'RESPONSABLE_VENTA_ID',
        'DESCUENTO': 'DESCUENTO_ID',
        'MEDIO_DE_PAGO': 'MEDIO_DE_PAGO_ID',
        'ELABORO': 'RESPONSABLE_VENTA_ID', # Este no seria una columna duplicada, corresponde a quien elaboro el certificado
        'PROCEDENCIA': 'PROCEDENCIA_ID'
    }, inplace=True)
normal_raw_df.to_excel(f'{CCS.db_tables}/VENTAS.xlsx', index=False)

#########################################

