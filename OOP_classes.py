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
    def clean_numer(self, work_df, column):
        work_df[column] = work_df[column].str.replace(r"\D", "", regex=True)
        return work_df

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
    def check_if_empty(self, df, column, id_column):
        print('*'*50)
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
        #has_no_val = id_invalid[~id_invalid.isin(id_valid)]

       
        for i, id in id_serie_with_value.items():
            self.find_replace_value(i, id, df, id_column, column)

    def check_if_empty(wdf, df, column, actions):
        
        for action in  actions:
            # Option when want to drop a invalid value
            if action == 'D':
                for i, id in has_no_val.items():
                    wdf = pd.concat([wdf, df.loc[[i]]], ignore_index=True)
                    df = df.drop(i, axis=0)
                    df = df.reset_index()

            # Option when want to perform data filling with null value you can customice it
            elif action == 'F':
                filling = 'null'
                if not has_value.empty:
                    print('Please perform a replacement!')
                
                for i, id in has_no_val.items():
                    df.loc[i, column] = filling

            # Option to capitalice the text
            elif action == 'C':
                df[column] = df[column].str.capitalize()

            # Option to capitalice every first letter
            elif action == 'T':
                df[column] = df[column].str.title()
            
            # opciton to uppercase the text
            elif action == 'U':
                df[column] = df[column].str.upper()

            else:
                print("Error! action parameter wrong.")

        return df, wdf


"""
This class will contain info related to the CCS_analisys and required methods
"""
class Project(DataPipeline):
    def __init__(self):
        self.config = "./Python-analisys/config.json" # Config file
        self.start_year = "2023" # this 2023 is for testing
        self.current_year = ""
        self.info_source_path = ""
        self.cleaned_path = ""
        self.rejected_path = ""
        self.work_folders = []
        self.work_files_per_year = {}

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
        return True

    # Method to get work folder per yer
    def find_work_foldes(self):
        self.work_folders = [name for name in os.listdir(self.info_source_path)
                             if os.path.isdir(os.path.join(self.info_source_path, name))]
        if not self.work_folders:
            return False
        return True
    
    # Method to get fields from the specified directory (need to specify the years) on var years
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
            ['CIUDAD/REGION'],
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
