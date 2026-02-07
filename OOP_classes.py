import pandas as pd
import json
import os
import re

from datetime import datetime

"""
This class allows you to perform basic data management before EDA
"""
class DataPipeline:
    def __init__(self):
        pass
    
    # Method 
    def clean_numer(self, number):
        return re.sub(r'\D', '', number)

    # Method to take configuration from .json file, return all items
    def read_config_json(self):
        with open(self.config, 'r') as archive:
            config = json.load(archive)
        # When config file is empty return a False
        if not config:
            return False
        # Return of config.json file
        return config

    def find_replace_value(self, i, id, df, id_column, column):
        value = df.loc[df[id_column] == id, column].dropna().iloc[0]
        df.loc[i, column] = value
    
    # function to find missing information in dataframe, find if any similar data exist to replace in missing one
    # parameter action [R(Raplace with similar values), D(drop missing values), F(fill missing values with null), C(To capitalize the text)]
    def check_if_empty(self, wrong_df, df, column, id_column, actions): #wdf, df, column, column2, actions
        print(f'Data cleaning for {column} column')
        
        # This mask will return al serie bool with values that being empty or NAN
        mask = df[column].apply(lambda x: str(x).strip() == '') | df[column].isna()
        # This serie will contain values that match with the missing valios in column_2
        id_without_values = df.loc[mask, id_column]
        # This serie will contain values that match with rows with info in column_2
        id_with_values = df.loc[~mask, id_column]
        # This serie will contain values that has a values despite has missing values in another row
        id_serie_with_value = id_without_values[id_without_values.isin(id_with_values)]
        # This serie will contain values that hasn't a value despite has missing values in another row
        id_serie_without_value = id_without_values[~id_without_values.isin(id_with_values)]

        for action in  actions:
            # Option when want to perform replacement with backup
            if action == 'R': #-> REPLACEMENT
                for i, id in id_serie_with_value.items():
                    self.find_replace_value(i, id, df, id_column, column)

            # Option when want to drop a invalid value
            elif action == 'D': #-> DROP
                for i, id in id_serie_without_value.items():
                    wrong_df = pd.concat([wrong_df, df.loc[[i]]], ignore_index=True)
                    df = df.drop(i, axis=0).reset_index(drop=True)

            # Option to perform data filling with null value you can customice it
            elif action == 'F': #-> FILL
                filling = 'null'
                if not id_serie_with_value.empty:
                    print('Please perform a replacement!')
                
                for i, id in id_serie_without_value.items():
                    df.loc[i, column] = filling

            # Option to capitalice the text
            elif action == 'C': #-> CAPITALICE
                #df[column] = df[column].str.capitalize()
                df[column] = df[column].astype(str).str.capitalize()


            # Option to capitalice every first letter
            elif action == 'T': #-> CAPITALICE FIRST LETTER
                #df[column] = df[column].str.title()
                df[column] = df[column].astype(str).str.title()

            
            # opciton to uppercase the text
            elif action == 'U': #-> UPPER CASE
                df[column] = df[column].str.upper()

            else:
                print("🤖❌ Error! action parameter wrong.")

        return df, wrong_df

    def replace_text(self, df, column, sre, ifno='null'):
        df[column] = df[column].map(sre).fillna(ifno)

    def store_output_files(self, cleaned_path, work_df, rejected_path, wrong_df, file):
        work_df.to_excel(cleaned_path+"/Cleaned_"+file[:-4]+"xlsx", index=False, engine="openpyxl")
        print('🤖​✅​​​ Archivo con datos tratados guardado!')
        if not wrong_df.empty:
            wrong_df.to_excel(rejected_path+"/Rejected_"+file[:-4]+"xlsx", index=False, engine="openpyxl")
            print('🤖​✅​ Archivo con datos erróneos guardado!')
    
    def normalize_column(self, raw_df, column, normalized_map):
        replaced = {}
        for standar, sinonims in normalized_map.items():
            for s in sinonims:
                replaced[s] = standar
        
        raw_df[column] = raw_df[column].apply(lambda x : replaced.get(x, x))
        return raw_df
    
## ---------------------------------------------------------------------------------
    """
    ##  Parameters  ##
    columnas_datos: lista que contiene los parametros de los cuales voy a extraer informacion
    id_column: Columna referencias, sera el id de los registro que busco dejar como unicos
    raw_consl_df: corresponde al dataframe que contiene la informacion
    ruta_archivo: contiene la ruta de la nueva tabla
    index: parametro necesario para indicar al script cual columna es el index
    """
    def table_creation(self, raw_consl_df, columnas_datos, id_column, ruta_archivo, index):
        print(f"🤖​ Creacion tabla {id_column} 🦾✍️​")
        # --- PARTE 1: SELECCIONAR LA FILA CON MÁS DATOS ---

        # Calculamos cuántos datos NO nulos tiene cada fila en las columnas de interés
        # Creamos una columna temporal 'calidad_datos'
        raw_consl_df['calidad_datos'] = raw_consl_df[columnas_datos].notna().sum(axis=1)

        # Ordenamos: Primero por ID, luego por 'calidad_datos' de mayor a menor (descending)
        # Así la fila con más datos queda arriba para cada ID
        df_sorted = raw_consl_df.sort_values(
            by=[id_column, 'calidad_datos'], 
            ascending=[True, False]
        )

        # Eliminamos duplicados por ID, quedándonos solo con la primera (la que tiene más datos)
        df_candidatos = df_sorted.drop_duplicates(subset=[id_column], keep='first')

        # Limpiamos: Seleccionamos solo las columnas finales y reseteamos el índice
        cols_finales = [id_column] + columnas_datos
        df_candidatos = df_candidatos[cols_finales].reset_index(drop=True)


        # --- PARTE 2: GESTIÓN DEL ARCHIVO EXCEL (INCREMENTAL) ---
        if os.path.exists(ruta_archivo):
            print("🤖​ El archivo ya existe. Verificando registros nuevos...")
            
            # Leemos el archivo existente
            df_existente = pd.read_excel(ruta_archivo, index_col=index)
            
            # Obtenemos los IDs que ya existen para no duplicarlos ni modificarlos
            ids_existentes = set(df_existente[id_column].astype(str))
            
            # Filtramos: Solo nos quedamos con los IDs de df_candidatos que NO están en el Excel
            # Convertimos a string para asegurar comparación correcta
            nuevos_registros = df_candidatos[~df_candidatos[id_column].astype(str).isin(ids_existentes)]
            
            if not nuevos_registros.empty:
                # Concatenamos los antiguos con los nuevos
                df_final = pd.concat([df_existente, nuevos_registros], ignore_index=True)
                # Guardamos todo el conjunto
                df_final.to_excel(ruta_archivo, index=True, index_label=index)
                print(f"🤖​ Se agregaron {len(nuevos_registros)} nuevos registros.")
                df_result = df_final # Para que puedas imprimir el resultado final si quieres
            else:
                print("🤖​ No hay registros nuevos para agregar.")
                df_result = df_existente

        else:
            print("🤖​ El archivo no existe. Creando uno nuevo...")
            df_candidatos.to_excel(ruta_archivo, index=True, index_label=index)
            df_result = df_candidatos

        print("*"*50)
        print(df_result.head(4))
## ---------------------------------------------------------------------------------


"""
This class will contain info related to the CCS_analisys and required methods
"""
class Project(DataPipeline):
    def __init__(self):
        self.config = "./config.json" # Config file
        self.start_year = "2024" # this year match with first data folder
        self.current_year = ""
        self.info_source_path = ""
        self.db_tables = ""
        self.cleaned_path = ""
        self.rejected_path = ""
        self.work_folders = []
        self.cleaned_work_files = []
        self.work_files_per_year = {}
        self.gender_sre = {
            'M': 'Masculino',
            'F': 'Femenino'
            }
        self.month_is = {
            'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4,
            'MAYO': 5, 'JUNIO': 6, 'JULIO': 7, 'AGOSTO': 8,
            'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
            }

    # Getters and Setters

    def get_start_year(self):
        return self.start_year
    
    def get_info_source_path(self):
        return self.info_source_path
    
    def get_cleaned_path(self):
        return self.info_source_path
    
    def get_rejected_path(self):
        return self.info_source_path
    
    def get_current_year(self):
        return self.current_year
    def set_current_year(self):
        self.current_year = str(datetime.now().year)


    # Methods

    # Inherited method, set attribute fro class Project
    def read_config_json(self):
        config = super().read_config_json()
        if not config:
            return False

        self.info_source_path = config['info_source']
        self.cleaned_path = config['cleaned']
        self.rejected_path = config['rejected']
        self.db_tables = config['tables']
        return True

    # Method to get work folder per yer
    def find_work_foldes(self):
        self.work_folders = [name for name in os.listdir(self.info_source_path)
                             if os.path.isdir(os.path.join(self.info_source_path, name))]
        if not self.work_folders:
            return False
        return True
    
    # Method to get fields from source path (need to specify the years) on var years
    def set_work_files_per_year(self):
        start_year = int(self.start_year)
        current_year = int(self.current_year)
        while start_year <= current_year:
            path = f"{self.info_source_path}/{start_year}"
            files = []
            for file in os.listdir(path):
                if file.endswith('.xlsm'):
                    files.append(file)
            self.work_files_per_year[str(start_year)] = files
            start_year += 1
    
    # Method to get fields from cleaned_path
    def consolidate_work_files_per_year(self):
        dfs = []
        for file in os.listdir(self.cleaned_path):
            if file.endswith('.xlsx'):
                file_path = os.path.join(self.cleaned_path, file)
                print('🤖​ Leyendo:', file_path)
                df = pd.read_excel(file_path)
                dfs.append(df)
        
        df_consolidate = pd.concat(dfs, ignore_index=True)
        df_consolidate.to_csv(f'{self.info_source_path}/tmp_consolidate.csv', index=False, encoding="utf-8")
        print('​​✅​ Archivo consolidado creado con exito!')
    
    # This method creates the column data structure for cosolidate sales file
    def re_organize_columns(self, work_df):
        temporary_df = pd.DataFrame()
        columns = work_df.columns.tolist()
        
        provided_order = [
            ['NUMERO DE IDENTIFICACION'],
            ['PRIMER APELLIDO'],
            ['SEGUNDO APELLIDO'],
            ['PRIMER NOMBRE'],
            ['SEGUNDO NOMBRE'],
            ['FECHA DE NACIMIENTO'],
            ['GENERO'],
            ['CELULAR'],
            ['CORREO'],
            ['CIUDAD REGION', 'CIUDAD/REGION'],
            ['PROFESION', 'PERFIL DEL PROFESIONAL'],
            ['CURSO'],
            ['MODALIDAD'],
            ['RENOVACION'],
            ['RESPONSABLE VENTA', 'RESPONSABLE'],
            ['FECHA DE VENTA'],
            ['VALOR UNITARIO'],
            ['DESCUENTO'],
            ['PRECIO NETO'],
            ['MEDIO DE PAGO'],
            ['FECHA DE PAGO'],
            ['ELABORO', 'REALIZADOR'],
            ['PROCEDENCIA'],
            ['SEGUIMIENTO POST-VENTA']
        ]
        
        for col in provided_order:
            for item in col:
                if item in columns:
                    values = work_df.pop(item)
                    temporary_df[col[0]] = values
                    break
            else:
                temporary_df[col[0]] = 'null'
        
        return temporary_df
