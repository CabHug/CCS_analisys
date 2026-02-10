import pandas as pd
import numpy as np
from OOP_classes import Project

# ==========================================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================================
CCS = Project()
CCS.set_current_year() 
CCS.read_config_json() 
CCS.find_work_foldes() 
CCS.set_work_files_per_year() 

# Cargamos el consolidado y hacemos una COPIA para no afectar el original
consl_df = pd.read_csv(f'{CCS.info_source_path}/consolidate_normalized.csv')
raw_consl_df = consl_df.copy()

# ==========================================================
# 2. FUNCIONES DE APOYO MEJORADAS
# ==========================================================

def consolidar_maestra(df, columna_id, columnas_datos):
    """
    Agrupa por ID y rescata la mejor información disponible.
    IMPORTANTE: Convierte vacíos a NaN para que .first() no tome celdas vacías como datos válidos.
    """
    temp = df[[columna_id] + columnas_datos].copy()
    
    # 1. Limpieza de ID
    temp[columna_id] = temp[columna_id].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    
    # 2. LIMPIEZA PROFUNDA: Convertir '', ' ', 'null', 'None' a np.nan (Nulo real)
    # Esto es vital para que Pandas ignore las celdas vacías y busque el dato real en las siguientes filas
    temp = temp.replace(r'^\s*$', np.nan, regex=True)
    temp = temp.replace(['nan', 'null', 'None'], np.nan)

    # 3. Agrupamos. .first() ahora saltará los NaNs y tomará el primer valor REAL.
    consolidado = temp.groupby(columna_id).first().reset_index()
    
    return consolidado

def mapear_categorias_corregida(df_ventas, df_lookup, columna_categoria, columna_id, columna_a_modificar=None):
    if columna_a_modificar is None:
        columna_a_modificar = columna_categoria

    # Limpieza para asegurar match (strip quita espacios invisibles al inicio/final)
    df_ventas[columna_a_modificar] = df_ventas[columna_a_modificar].astype(str).str.strip()
    df_lookup[columna_categoria] = df_lookup[columna_categoria].astype(str).str.strip()

    mapa_ids = df_lookup.set_index(columna_categoria)[columna_id]
    
    # Mapeamos. Si no encuentra el ID, dejará NaN (que luego el script CSV convertirá a 0 o null)
    df_ventas[columna_a_modificar] = df_ventas[columna_a_modificar].map(mapa_ids)
    
    return df_ventas

# ==========================================================
# 3. CREACIÓN DE TABLAS MAESTRAS
# ==========================================================
print("*"*50)
print("## ​​​🤖​ CONSOLIDACIÓN Y CREACIÓN DE TABLAS ​​​🤖​ ##")
print("*"*50)

# --- A. CLIENTES (Corrección del Correo perdido) ---
print("🤖 Consolidando CLIENTES (Priorizando datos no vacíos)...")
cols_clientes = ['PRIMER_APELLIDO', 'SEGUNDO_APELLIDO', 'PRIMER_NOMBRE', 'SEGUNDO_NOMBRE', 
                 'FECHA_DE_NACIMIENTO', 'GENERO', 'CELULAR', 'CORREO', 'CIUDAD_REGION', 'PROFESION']

df_clientes_full = consolidar_maestra(raw_consl_df, 'NUMERO_DE_IDENTIFICACION', cols_clientes)

# Insertamos ID
df_clientes_full.insert(0, 'CLIENTE_ID', range(1, len(df_clientes_full) + 1))

# Guardamos
ruta_cli = f'{CCS.db_tables}/a_base/CLIENTES.xlsx'
df_clientes_full.to_excel(ruta_cli, index=False)
CCS.table_creation(df_clientes_full, cols_clientes, 'NUMERO_DE_IDENTIFICACION', ruta_cli, 'CLIENTE_ID')

# --- B. CURSOS ---
print("🤖 Consolidando CURSOS...")
df_cursos = consolidar_maestra(raw_consl_df, 'CURSO', ['VALOR_UNITARIO'])
ruta_cur = f'{CCS.db_tables}/CURSO.xlsx'
CCS.table_creation(df_cursos, ['VALOR_UNITARIO'], 'CURSO', ruta_cur, 'CURSO_ID')

# --- C. RESPONSABLE DE VENTA (Corrección para ELABORO) ---
print("🤖 Creando lista maestra de EMPLEADOS (Ventas + Elaboró)...")
# Unimos las dos columnas para tener TODOS los nombres posibles
vendedores = raw_consl_df['RESPONSABLE_VENTA'].dropna().unique()
elaboradores = raw_consl_df['ELABORO'].dropna().unique()
# Concatenamos y quitamos duplicados
todos_los_empleados = pd.DataFrame(np.unique(np.concatenate((vendedores, elaboradores))), columns=['RESPONSABLE_VENTA'])

ruta_resp = f'{CCS.db_tables}/RESPONSABLE_VENTA.xlsx'
# Usamos este dataframe combinado para crear la tabla maestra
CCS.table_creation(todos_los_empleados, [], 'RESPONSABLE_VENTA', ruta_resp, 'RESPONSABLE_VENTA_ID')

# --- D. OTRAS MAESTRAS SIMPLES ---
otras_maestras = {
    'PROFESION': 'PROFESION_ID', 'MODALIDAD': 'MODALIDAD_ID', 'GENERO': 'GENERO_ID',
    'MEDIO_DE_PAGO': 'MEDIO_DE_PAGO_ID', 'PROCEDENCIA': 'PROCEDENCIA_ID',
    'CIUDAD_REGION': 'CIUDAD_REGION_ID', 'DESCUENTO': 'DESCUENTO_ID'
}

for tabla, id_name in otras_maestras.items():
    print(f"🤖 Procesando: {tabla}")
    ruta = f'{CCS.db_tables}/{tabla}.xlsx'
    CCS.table_creation(raw_consl_df, [], tabla, ruta, id_name)

# ==========================================================
# 4. NORMALIZACIÓN DE CLIENTES (IDs Externos)
# ==========================================================
print("\n🤖 Actualizando IDs en tabla CLIENTES...")
df_clientes_final = pd.read_excel(f'{CCS.db_tables}/a_base/CLIENTES.xlsx')

for col in ['CIUDAD_REGION', 'GENERO', 'PROFESION']:
    df_ref = pd.read_excel(f'{CCS.db_tables}/{col}.xlsx')
    df_clientes_final = mapear_categorias_corregida(df_clientes_final, df_ref, col, f'{col}_ID')

df_clientes_final.rename(columns={'CIUDAD_REGION': 'CIUDAD_REGION_ID', 'GENERO': 'GENERO_ID', 'PROFESION': 'PROFESION_ID'}, inplace=True)
df_clientes_final.to_excel(f"{CCS.db_tables}/CLIENTES.xlsx", index=False)

# ==========================================================
# 5. CREACIÓN DE FACT_VENTAS
# ==========================================================
print("\n🤖 Generando FACT_VENTAS (Mapeando todos los IDs)...")
df_ventas = raw_consl_df.copy()

# Mapeos estándar
cols_map = ['CURSO', 'DESCUENTO', 'MEDIO_DE_PAGO', 'MODALIDAD', 'PROCEDENCIA']
for col in cols_map:
    df_ref = pd.read_excel(f'{CCS.db_tables}/{col}.xlsx')
    df_ventas = mapear_categorias_corregida(df_ventas, df_ref, col, f'{col}_ID')

# Mapeo Clientes
df_cli = pd.read_excel(f'{CCS.db_tables}/CLIENTES.xlsx')
# Convertimos a string para asegurar match
df_cli['NUMERO_DE_IDENTIFICACION'] = df_cli['NUMERO_DE_IDENTIFICACION'].astype(str).str.replace(r'\.0$', '', regex=True)
df_ventas['NUMERO_DE_IDENTIFICACION'] = df_ventas['NUMERO_DE_IDENTIFICACION'].astype(str).str.replace(r'\.0$', '', regex=True)
df_ventas = mapear_categorias_corregida(df_ventas, df_cli, 'NUMERO_DE_IDENTIFICACION', 'CLIENTE_ID')

# Mapeo RESPONSABLE Y ELABORO (Ambos usan la misma tabla maestra ahora completa)
df_resp = pd.read_excel(f'{CCS.db_tables}/RESPONSABLE_VENTA.xlsx')
print("   -> Mapeando Responsable Venta...")
df_ventas = mapear_categorias_corregida(df_ventas, df_resp, 'RESPONSABLE_VENTA', 'RESPONSABLE_VENTA_ID')

print("   -> Mapeando Elaboró...")
# Aquí usamos la misma tabla de referencia, pero aplicamos el ID sobre la columna 'ELABORO'
df_ventas = mapear_categorias_corregida(df_ventas, df_resp, 'RESPONSABLE_VENTA', 'RESPONSABLE_VENTA_ID', columna_a_modificar='ELABORO')

# Selección final
df_final = df_ventas[[
    'NUMERO_DE_IDENTIFICACION', 'CURSO', 'MODALIDAD', 'RENOVACION', 
    'RESPONSABLE_VENTA', 'FECHA_DE_VENTA', 'DESCUENTO', 'PRECIO_NETO', 
    'MEDIO_DE_PAGO', 'FECHA_DE_PAGO', 'ELABORO', 'PROCEDENCIA', 'SEGUIMIENTO_POST-VENTA'
]]

df_final.columns = [
    'CLIENTE_ID', 'CURSO_ID', 'MODALIDAD_ID', 'RENOVACION', 
    'RESPONSABLE_VENTA_ID', 'FECHA_DE_VENTA', 'DESCUENTO_ID', 'PRECIO_NETO', 
    'MEDIO_DE_PAGO_ID', 'FECHA_DE_PAGO', 'ELABORO', 'PROCEDENCIA_ID', 'SEGUIMIENTO_POST-VENTA'
]

# Guardar
df_final.to_excel(f'{CCS.db_tables}/VENTAS.xlsx', index=True, index_label='VENTA_ID')
print("\n✨ PROCESO FINALIZADO - Revisa CLIENTES.xlsx y VENTAS.xlsx ✨")