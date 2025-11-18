import pandas as pd
import json
import os


from datetime import datetime



"""
This class will contain info related to the CCS_analisys
"""
class project:
    def __init__(self):
        self.config = "./Python-analisys/config.json"
        self.start_year = "2024"
        self.current_year = ""
        self.info_source_path = ""
        self.cleaned_path = ""
        self.rejected_path = ""
        self.work_folders = []

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

    def read_config_json(self):
        with open(self.config, 'r') as archive:
            config = json.load(archive)

        if not config:
            return False

        self.info_source_path = config['info_source']
        self.cleaned_path = config['cleaned']
        self.rejected_path = config['rejected']
        return True

    def find_work_foldes(self):
        self.work_folders = [name for name in os.listdir(self.info_source_path)
                             if os.path.isdir(os.path.join(self.info_source_path, name))]
        if not self.work_folders:
            return False
        return True


CCS = project()
CCS.set_current_year()

print(CCS.get_current_year())
print(CCS.read_config_json())
print(CCS.find_work_foldes())

