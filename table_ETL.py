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
"""
df_result = raw_consl_df.groupby('NUMERO_DE_IDENTIFICACION', as_index=False)[['PRIMER_APELLIDO', 'SEGUNDO_APELLIDO', 'PRIMER_NOMBRE', 'SEGUNDO_NOMBRE', 'FECHA_DE_NACIMIENTO', 'GENERO', 'CELULAR', 'CORREO', 'CIUDAD/REGION', 'PROFESION']].first()
df_result.to_excel(f'{CCS.db_tables}/CLIENTES.xlsx', index=True, index_label="CLIENTE_ID")
print(df_result)
print("*"*50)
"""
columnas_datos = ['PRIMER_APELLIDO', 'SEGUNDO_APELLIDO', 'PRIMER_NOMBRE', 
                  'SEGUNDO_NOMBRE', 'FECHA_DE_NACIMIENTO', 'GENERO', 
                  'CELULAR', 'CORREO', 'CIUDAD/REGION', 'PROFESION']
ruta_archivo = f'{CCS.db_tables}/CLIENTES.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'NUMERO_DE_IDENTIFICACION', ruta_archivo, 'CLIENTE_ID')

## CREACION DE TABLA PROFESION
"""
df_result = pd.DataFrame({'PROFESION': raw_consl_df['PROFESION'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/PROFESION.xlsx', index=True, index_label="PROFESION_ID")
print(df_result)
print("*" * 50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/PROFESION.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'PROFESION', ruta_archivo, 'PROFESION_ID')

## CREACION DE TABLA MODALIDAD
"""
df_result = pd.DataFrame({'MODALIDAD': raw_consl_df['MODALIDAD'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/MODALIDAD.xlsx', index=True, index_label="MODALIDAD_ID")
print(df_result)
print("*" * 50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/MODALIDAD.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'MODALIDAD', ruta_archivo, 'MODALIDAD_ID')

## CREACION DE TABLA GENERO
"""
df_result = pd.DataFrame({'GENERO': raw_consl_df['GENERO'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/GENERO.xlsx', index=True, index_label="GENERO_ID")
print(df_result)
print("*" * 50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/GENERO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'GENERO', ruta_archivo, 'GENERO_ID')

## CREACION DE TABLA RESPONSABLE_VENTA
"""
df_result = pd.DataFrame({'RESPONSABLE_VENTA': raw_consl_df['RESPONSABLE_VENTA'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/RESPONSABLE_VENTA.xlsx', index=True, index_label="RESPONSABLE_VENTA_ID")
print(df_result)
print("*" * 50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/RESPONSABLE_VENTA.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'RESPONSABLE_VENTA', ruta_archivo, 'RESPONSABLE_VENTA_ID')

## CREACION DE TABLA MEDIO_DE_PAGO
"""
df_result = pd.DataFrame({'MEDIO_DE_PAGO': raw_consl_df['MEDIO_DE_PAGO'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/MEDIO_DE_PAGO.xlsx', index=True, index_label="MEDIO_DE_PAGO_ID")
print(df_result)
print("*" * 50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/MEDIO_DE_PAGO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'MEDIO_DE_PAGO', ruta_archivo, 'MEDIO_DE_PAGO_ID')

## CREACION DE TABLA PROCEDENCIA
"""
df_result = pd.DataFrame({'PROCEDENCIA': raw_consl_df['PROCEDENCIA'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/PROCEDENCIA.xlsx', index=True, index_label="PROCEDENCIA_ID")
print(df_result)
print("*" * 50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/PROCEDENCIA.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'PROCEDENCIA', ruta_archivo, 'PROCEDENCIA_ID')

## CREACION DE TABLA CURSOS
"""
df_result = raw_consl_df.groupby('CURSO', as_index=False)['VALOR_UNITARIO'].first()
df_result.to_excel(f'{CCS.db_tables}/CURSOS.xlsx', index=True, index_label="CURSO_ID")
print(df_result)
print("*"*50)
"""
columnas_datos = ['VALOR_UNITARIO']
ruta_archivo = f'{CCS.db_tables}/CURSO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'CURSO', ruta_archivo, 'CURSO_ID')

## CREACION DE TABLA CIUDAD_REGION
"""
df_result = pd.DataFrame({'CIUDAD/REGION': raw_consl_df['CIUDAD/REGION'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/CIUDAD_REGION.xlsx', index=True, index_label="CIUDAD/REGION_ID")
print(df_result)
print("*"*50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/CIUDAD_REGION.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'CIUDAD_REGION', ruta_archivo, 'CIUDAD_REGION_ID')

## CREACION DE TABLA CIUDAD_REGION
"""
df_result = pd.DataFrame({'DESCUENTO': raw_consl_df['DESCUENTO'].unique()}).sort_index()
df_result.to_excel(f'{CCS.db_tables}/DESCUENTO.xlsx', index=True, index_label="DESCUENTO_ID")
print(df_result)
print("*" * 50)
"""
columnas_datos = []
ruta_archivo = f'{CCS.db_tables}/DESCUENTO.xlsx'
CCS.table_creation(raw_consl_df, columnas_datos, 'DESCUENTO', ruta_archivo, 'DESCUENTO_ID')

## CREACION DE TABLA DE VENTAS TOTALES
def mapear_categorias(df_ventas, df_categorias_lookup, columna_categoria):
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
    mapa_ids = df_categorias_lookup.set_index(columna_categoria).index.to_series()
    categorias_en_ventas = set(df_ventas[columna_categoria].unique())
    categorias_en_lookup = set(df_categorias_lookup[columna_categoria].unique())
    categorias_faltantes = categorias_en_ventas - categorias_en_lookup

    if categorias_faltantes:
        print("*" * 50)
        print("🤖🚨 ERROR DE CATEGORÍA NO ENCONTRADA")
        print(f"🤖 Las siguientes categorías en '{columna_categoria}' no existen en la tabla de referencia:")
        print(categorias_faltantes)
        print("-" * 50)
        
        # Opcional: Mostrar los registros específicos que están mal
        registros_malos = df_ventas[df_ventas[columna_categoria].isin(categorias_faltantes)]
        print("🤖 Registros de ventas afectados:")
        print(registros_malos)
        print("*" * 50)
        
        # Detenemos la función y levantamos un error
        raise ValueError("🤖 El mapeo no se puede completar debido a categorías faltantes.")
        
    df_ventas['ID_' + columna_categoria.upper()] = df_ventas[columna_categoria].map(mapa_ids)
    
    return df_ventas

raw_conslidate_df = pd.read_csv(f'{CCS.info_source_path}/consolidate_normalized.csv')
work_tables = [name for name in os.listdir(CCS.db_tables)]

for table in work_tables:
    print(table)
    if table == 'CLIENTES.xlsx':
        continue
    category = str(table[:-5])
    print(f'🤖 ID normalizacion para la categoria: {category}')
    df_categorias_lookup = pd.read_excel(f'{CCS.db_tables}/{table}')
    try:
        df_ventas_mapeadas = mapear_categorias(
            raw_conslidate_df.copy(),
            df_categorias_lookup.copy(), 
            category
        )
        print("\n🤖✅ Mapeo completado exitosamente.")
        print(df_ventas_mapeadas)
    except ValueError as e:
        print(f"\n🤖⚠️ Mapeo fallido: {e}")