import pandas as pd

from OOP_classes import *

# Main object definition of CSS project
CCS = Project()
# Strating with CSS object configuration
CCS.set_current_year() # Set current year in object attributes
CCS.read_config_json() # Set paths required for Extract data files
CCS.find_work_foldes() # Set work folders inside data_source folder
CCS.set_work_files_per_year() # Create a dictionario with work files per year



print(CCS.work_files_per_year['2023'])

# cycle for capture each year
for year in ['2023']:#-> 2023 testing <-#
    # cycle to read each document
    for file in CCS.work_files_per_year[year]:
        print(file)
        # Take info (data_source, year and file) to build the path
        work_df = pd.read_excel(f'{CCS.get_info_source_path()}/{year}/{file}')
        # New dataframe to store wrong data from each file
        wrong_df = pd.DataFrame(columns=work_df.columns)
        # Cleaning headers of hidden spaces
        work_df.columns = work_df.columns.str.strip()
        # Remove the first row from work dataframe (docuemnt's index column)
        work_df.drop(work_df.columns[0], axis=1, inplace=True)

        print(work_df.head())

        # Reorganize columns to have a better order
        work_df = CCS.re_organize_columns(work_df)

        

        print(work_df.head())