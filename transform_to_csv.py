import pandas as pd
import os

from OOP_classes import *

CCS = Project()
# Strating with CCS object configuration
CCS.set_current_year() # Set current year in object attributes
CCS.read_config_json() # Set paths required for Extract data files
CCS.find_work_foldes() # Set work folders inside data_source folder
CCS.set_work_files_per_year() # Create a dictionario with work files per year

import pandas as pd
import os

def convertir_xlsx_a_csv_final_con_limpieza_numerica(ruta_origen, ruta_destino):
    """
    Busca archivos .xlsx, normaliza los formatos de fecha, y garantiza que 
    las columnas críticas (como precios) no contengan 'null' si deben ser NUMERIC.
    """
    if not os.path.isdir(ruta_origen):
        print(f"❌ Error: La ruta de origen '{ruta_origen}' no es un directorio válido.")
        return

    # 1. Crear la carpeta de destino si no existe
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
        print(f"📁 Creada carpeta de destino: {ruta_destino}")

    print(f"\n🔎 Procesando archivos de origen: {ruta_origen}")

    # Columnas de fecha a revisar, asumiendo el formato de origen DD/MM/YYYY
    columnas_fecha = ['FECHA_DE_NACIMIENTO', 'FECHA_DE_VENTA', 'FECHA_DE_PAGO']
    
    # NUEVO: Columnas numéricas obligatorias que NO deben ser 'null' en PG
    columnas_numericas_obligatorias = ['PRECIO_NETO', 'VALOR_UNITARIO']

    for nombre_archivo in os.listdir(ruta_origen):
        if nombre_archivo.lower().endswith('.xlsx'):

            ruta_xlsx = os.path.join(ruta_origen, nombre_archivo)
            nombre_csv = nombre_archivo.replace('.xlsx', '.csv').replace('.XLSX', '.csv')
            ruta_csv = os.path.join(ruta_destino, nombre_csv)

            try:
                df = pd.read_excel(ruta_xlsx)
                
                # 2. Normalización de Fechas
                for col in columnas_fecha:
                    if col in df.columns:
                        df[col] = pd.to_datetime(
                            df[col], 
                            format='%d/%m/%Y',
                            errors='coerce'
                        )
                        print(f"    🔄 Columna '{col}' convertida a formato SQL.")
                
                # 3. MODIFICACIÓN CLAVE: Rellenar nulos en columnas NUMÉRICAS
                for col_num in columnas_numericas_obligatorias:
                    if col_num in df.columns:
                        # Reemplazamos cualquier NaN o valor no numérico con 0
                        df[col_num] = pd.to_numeric(df[col_num], errors='coerce').fillna(0)
                        print(f"    💵 Columna '{col_num}' rellenada con 0 para evitar error NUMERIC: 'null'.")

                # 4. Guardar como CSV, con manejo de nulos (SOLO para columnas no numéricas obligatorias)
                # na_rep='null' ahora solo afecta a las columnas de texto o fechas fallidas
                df.to_csv(
                    ruta_csv, 
                    index=False, 
                    encoding='utf-8', 
                    na_rep='null' # Rellena otros nulos (texto, fechas fallidas) con 'null'
                )
                
                print(f"  ✅ Convertido '{nombre_archivo}'.")
                
            except Exception as e:
                print(f"  ❌ Error al procesar {nombre_archivo}: {e}")
                
    print("\nProceso de conversión finalizado. Los CSV están listos para PostgreSQL.")
convertir_xlsx_a_csv_final_con_limpieza_numerica(CCS.db_tables, f'{CCS.db_tables}/a_csv_tables')