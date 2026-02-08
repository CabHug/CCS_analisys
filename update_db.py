import os
import pandas as pd
from sqlalchemy import create_engine, text
from io import StringIO

from OOP_classes import Project
CCS = Project()
CCS.read_config_json()


# ==============================================================================
# --- CONFIGURACIÓN DE CONEXIÓN (PON TU INFORMACIÓN AQUÍ) ---
# ==============================================================================
DB_USER = CCS.db_config['user']
DB_PASS = CCS.db_config['password']
DB_HOST = CCS.db_config['host']
DB_PORT = CCS.db_config['port']
DB_NAME = CCS.db_config['database']  # Asegúrate de que este es el nombre de tu DB
SCHEMA_NAME = 'public' # Por defecto es 'public', cámbialo si creaste un esquema propio
# ==============================================================================

# --- CONFIGURACIÓN DE RUTAS ---
RUTA_ARCHIVOS = r"C:\Users\Hugo\OneDrive\Documentos\MEGA\PROYECTOS\CCS\Analisis CCS\Python-analisys\DB_tables\a_csv_tables"

MAPEO_TABLAS = {
    'CIUDAD_REGION': 'ciudad_region',
    'CURSO': 'cursos',
    'DESCUENTO': 'descuento',
    'GENERO': 'genero',
    'MEDIO_DE_PAGO': 'medio_de_pago',
    'MODALIDAD': 'modalidad',
    'PROCEDENCIA': 'procedencia',
    'PROFESION': 'profesion',
    'RESPONSABLE_VENTA': 'responsable_venta',
    'CLIENTES': 'clientes',
    'VENTAS': 'fact_ventas'
}

def cargar_datos():
    # Cadena de conexión corregida
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}', pool_pre_ping=True)
    
    if not os.path.exists(RUTA_ARCHIVOS):
        print(f"❌ La ruta no existe: {RUTA_ARCHIVOS}")
        return

    archivos_en_carpeta = os.listdir(RUTA_ARCHIVOS)
    
    for nombre_base, tabla_destino in MAPEO_TABLAS.items():
        archivo_encontrado = [f for f in archivos_en_carpeta if f.upper().startswith(nombre_base)]
        
        if not archivo_encontrado:
            continue
            
        ruta_completa = os.path.join(RUTA_ARCHIVOS, archivo_encontrado[0])
        print(f"\n🚀 Procesando {archivo_encontrado[0]} -> Tabla {tabla_destino}...")

        try:
            # Leemos el CSV
            df = pd.read_csv(ruta_completa, sep=',', encoding='utf-8', engine='python')
            
            # --- 1. LIMPIEZA ---
            df.columns = [c.strip().upper() for c in df.columns]
            df.columns = [c.strip().upper().replace("-", "_") for c in df.columns]
            
            if tabla_destino == 'fact_ventas' and 'RESPONSABLE_VENTA_ID.1' in df.columns:
                df = df.rename(columns={'RESPONSABLE_VENTA_ID.1': 'ELABORO'})

            # --- 2. MANEJO DE NULOS (CRÍTICO PARA POSTGRES) ---
            # En lugar de texto "null", usamos None para que SQL reciba NULL real
            df = df.replace(['null', 'nan', 'NaN', 'None', ''], None)
            
            # --- 3. CONVERSIÓN DE TIPOS ---
            columnas_fecha = [c for c in df.columns if 'FECHA' in c]
            for col in columnas_fecha:
                df[col] = pd.to_datetime(df[col], errors='coerce')

            # Si definiste RENOVACION como VARCHAR(10) en el SQL:
            if 'RENOVACION' in df.columns:
                df['RENOVACION'] = df['RENOVACION'].apply(lambda x: 'Sí' if str(x).upper() in ['TRUE', '1', 'S', 'SI'] else 'No')

            # --- 4. CARGA ---
            with engine.begin() as conn:
                tabla_temp = f"temp_{tabla_destino}"
                
                # Cargamos a una tabla temporal
                df.to_sql(tabla_temp, conn, schema=SCHEMA_NAME, if_exists='replace', index=False)
                
                # Preparamos las columnas para el INSERT
                columnas_dest = ", ".join([f'"{c}"' for c in df.columns])
                
                # Casteo automático para fechas en la selección
                cols_origen_list = []
                for c in df.columns:
                    if 'FECHA' in c:
                        cols_origen_list.append(f'"{c}"::DATE')
                    else:
                        cols_origen_list.append(f'"{c}"')
                
                columnas_origen = ", ".join(cols_origen_list)
                pk_columna = df.columns[0] # Se asume que la primera columna es la PK (ID)

                # UPSERT: Inserta si no existe, o actualiza si ya existe (opcional)
                # Si prefieres solo insertar nuevos, usa 'DO NOTHING'
                query_upsert = text(f"""
                    INSERT INTO "{SCHEMA_NAME}"."{tabla_destino}" ({columnas_dest})
                    SELECT {columnas_origen} FROM "{SCHEMA_NAME}"."{tabla_temp}"
                    ON CONFLICT ("{pk_columna}") DO NOTHING;
                """)
                
                conn.execute(query_upsert)
                conn.execute(text(f'DROP TABLE "{SCHEMA_NAME}"."{tabla_temp}"'))
                
            print(f"✅ Éxito: {len(df)} registros procesados para {tabla_destino}")

        except Exception as e:
            print(f"❌ Error en {nombre_base}: {str(e)}")

if __name__ == "__main__":
    cargar_datos()