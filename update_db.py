import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from OOP_classes import Project

# ==========================================================
# 1. CONFIGURACIÓN Y RUTAS
# ==========================================================
CCS = Project()
CCS.read_config_json()

# Configuración de base de datos
DB_URL = f"postgresql://{CCS.db_config['user']}:{CCS.db_config['password']}@{CCS.db_config['host']}:{CCS.db_config['port']}/{CCS.db_config['database']}"
SCHEMA_NAME = 'public'

# Ruta de archivos CSV
RUTA_CSV_CARGA = r"C:\Users\Hugo\OneDrive\Documentos\MEGA\PROYECTOS\CCS\Analisis CCS\Python-analisys\DB_tables\a_csv_tables"

# Mapeo exacto CSV -> Tabla DB
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

# Orden de carga estricto
ORDEN_CARGA = [
    'ciudad_region', 'cursos', 'descuento', 'genero', 'medio_de_pago', 
    'modalidad', 'procedencia', 'profesion', 'responsable_venta', 
    'clientes', 'fact_ventas'
]

# ==========================================================
# 2. FUNCIONES DE APOYO
# ==========================================================

def limpiar_db(engine):
    """ Borra contenido y reinicia contadores SERIAL """
    print("\n🧹 LIMPIANDO BASE DE DATOS (TRUNCATE)...")
    with engine.begin() as conn:
        for tabla in reversed(ORDEN_CARGA):
            try:
                conn.execute(text(f'TRUNCATE TABLE "{SCHEMA_NAME}"."{tabla}" RESTART IDENTITY CASCADE;'))
            except Exception as e:
                print(f"   ⚠️ No se pudo limpiar {tabla}: {e}")
    print("✨ Base de datos lista.")

def validar_llaves_foraneas(df, tabla_nombre, engine):
    """ 
    Evita el error ForeignKeyViolation comparando con lo que ya se subió a la DB.
    Si un ID no existe en la maestra, se pone como None.
    """
    if tabla_nombre == 'clientes':
        maestras = {
            'GENERO_ID': 'genero',
            'PROFESION_ID': 'profesion',
            'CIUDAD_REGION_ID': 'ciudad_region'
        }
    elif tabla_nombre == 'fact_ventas':
        maestras = {
            'CLIENTE_ID': 'clientes',
            'CURSO_ID': 'cursos',
            'MODALIDAD_ID': 'modalidad',
            'DESCUENTO_ID': 'descuento',
            'MEDIO_DE_PAGO_ID': 'medio_de_pago',
            'PROCEDENCIA_ID': 'procedencia',
            'RESPONSABLE_VENTA_ID': 'responsable_venta',
            'ELABORO': 'responsable_venta'
        }
    else:
        return df

    for col_id, tabla_ref in maestras.items():
        if col_id in df.columns:
            # Consultar IDs existentes en la DB
            query = text(f'SELECT "{col_id if col_id != "ELABORO" else "RESPONSABLE_VENTA_ID"}" FROM "{SCHEMA_NAME}"."{tabla_ref}"')
            ids_validos = pd.read_sql(query, engine).iloc[:, 0].tolist()
            
            # Si el ID no está en los válidos, poner None
            invalidos = df[~df[col_id].isin(ids_validos) & df[col_id].notnull()]
            if not invalidos.empty:
                print(f"   ⚠️ Corrigiendo {len(invalidos)} huérfanos en {col_id} (referencia a {tabla_ref} no encontrada)")
                df.loc[~df[col_id].isin(ids_validos), col_id] = None
    return df

# ==========================================================
# 3. PROCESO PRINCIPAL
# ==========================================================

def cargar_datos():
    engine = create_engine(DB_URL)
    limpiar_db(engine)

    archivos_en_carpeta = os.listdir(RUTA_CSV_CARGA)
    mapeo_inverso = {v: k for k, v in MAPEO_TABLAS.items()}

    print("\n🚀 CARGANDO TABLAS...")

    for tabla_destino in ORDEN_CARGA:
        nombre_base = mapeo_inverso.get(tabla_destino)
        archivo = [f for f in archivos_en_carpeta if f.upper().startswith(nombre_base)]
        
        if not archivo:
            continue
            
        ruta = os.path.join(RUTA_CSV_CARGA, archivo[0])
        try:
            df = pd.read_csv(ruta, sep=',', encoding='utf-8', engine='python')
            df.columns = [c.strip().upper().replace("-", "_") for c in df.columns]

            # Renombrar campo especial en ventas
            if tabla_destino == 'fact_ventas' and 'RESPONSABLE_VENTA_ID.1' in df.columns:
                df = df.rename(columns={'RESPONSABLE_VENTA_ID.1': 'ELABORO'})

            # 1. Limpieza de Nulos en columnas obligatorias
            col_validar = tabla_destino.upper()
            if col_validar in df.columns:
                df = df.dropna(subset=[col_validar])

            # 2. Convertir vacíos a None para SQL
            df = df.replace({np.nan: None, 'null': None, 'NaN': None, '': None})

            # 3. Formatear fechas
            for col in [c for c in df.columns if 'FECHA' in c]:
                df[col] = pd.to_datetime(df[col], errors='coerce')

            # 4. PROTECCIÓN DE LLAVES FORÁNEAS (Evita el error que tuviste)
            df = validar_llaves_foraneas(df, tabla_destino, engine)

            # 5. Envío a Base de Datos
            df.to_sql(tabla_destino, engine, schema=SCHEMA_NAME, if_exists='append', index=False)
            print(f"   ✅ {tabla_destino.upper()}: {len(df)} filas.")

        except Exception as e:
            print(f"   ❌ ERROR en {tabla_destino}: {e}")
            return # Detener para evitar inconsistencias

if __name__ == "__main__":
    cargar_datos()
    print("\n🏁 Proceso finalizado.")