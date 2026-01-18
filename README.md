# CCS analisys

This proyect generate the tables that build the data base of CCS busness,
The data source will be stored in data source folder, each year will has it own folder
(i.e. 2026) the document of the month will be stored there with the next format
CCS_YYYY_Month.xlsm, the proyect has thre main scripts

## 1. ETL.py
This script takes the data directly from source file, add new columns, complete missing data
taking data from similar records, normalice recors due to some data has differents names but it's meaning
is the same, the output will be a file structured for each file processed.

## 2. Table_ETL.py
This script takes the files with cleaned data and creates each data base table, the information into each table
will be update with new records added in every script excecution, the outpur will be 11 tables
[ciudad_region, clientes, curso, desceunto, genero, medio_de_pago, modalidad, procedencia, profesion
responsable_ventas, ventas]

## 3. transform_to_csv.py
This script crate tables in a .csv format ready to upload in power BI report 

## 4. menu.py
This script makes easy the data process showing an interactive menu to the user, and asking for the next step that you what to run
in the pipe line data process

the common order to excecuted in the menu is:
- 1. Read raw data ETL
- 2. Table creation ETL
- 3. Convert table to csv