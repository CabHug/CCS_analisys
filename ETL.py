import pandas as pd
import os

from OOP_classes import Project
from normaize_map import NormalMap

# Main object definition of CCS project
CCS = Project()
# Strating with CCS object configuration
CCS.set_current_year() # Set current year in object attributes
CCS.read_config_json() # Set paths required for Extract data files
CCS.find_work_foldes() # Set work folders inside data_source folder
CCS.set_work_files_per_year() # Create a dictionario with work files per year (getting raw data)
#print(CCS.work_files_per_year)


# cycle for capture each year
for y in CCS.work_files_per_year:#-> start on 2024 <-#
    # cycle to read and clean each document
    for file in CCS.work_files_per_year[y]:
        print('*'*50)
        print(f"#-> Procesando archivo: {file}")
        f_year = file.split('_')[1]
        f_month = CCS.month_is[file.split('_')[2][:-5]]
        # Take info (data_source, year and file) to build the path
        work_df = pd.read_excel(f'{CCS.get_info_source_path()}/{y}/{file}')
        
        # FORZAR ENTEROS: Evita errores de tipo (int vs str) al comparar con los componentes de dt
        f_year_int = int(f_year)
        f_month_int = int(f_month)

        # New dataframe to store wrong data from each file
        wrong_df = pd.DataFrame(columns=work_df.columns)

        # Cleaning headers of hidden spaces
        work_df.columns = work_df.columns.str.strip()

        # Remove the first row from work dataframe (docuemnt's index column)
        work_df.drop(work_df.columns[0], axis=1, inplace=True)

        # Reorganize columns to have a better order
        work_df = CCS.re_organize_columns(work_df)

        ### START DATA CLEANING LOGIC ###
        headListIter = iter(list(work_df.columns))

         # 'NUMERO DE IDENTIFICACION' FIELD
        id_column = next(headListIter)
        work_df[id_column] = work_df[id_column].apply(lambda num : CCS.clean_numer(num))
        work_df = work_df.dropna(subset=[id_column])
        work_df = work_df[work_df[id_column].apply(lambda x : str(x).strip() !='')]

        # 'PRIMER APELLIDO' FIELD
        fst_last_name = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, fst_last_name, id_column, ['R','C','D'])

        # 'SEGUNDO APELLIDO' FIELD
        scd_last_name = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, scd_last_name, id_column, ['R','C','F'])
        
        # 'PRIMER NOMBRE' FIELD
        fst_name = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, fst_name, id_column, ['R','C','D'])

        # 'SEGUNDO NOMBRE' FIELD
        scd_name = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, scd_name, id_column, ['R','C','F'])

        # 'FECHA DE NACIMIENTO' FIELD
        brn_date = next(headListIter)
        work_df[brn_date] = pd.to_datetime(work_df[brn_date], errors='coerce')
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, brn_date, id_column, ['R'])
        work_df[brn_date] = work_df[brn_date].fillna(pd.Timestamp('01/01/1900'))  # Fill with a default date if NaT
        work_df[brn_date] = work_df[brn_date].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

        # 'GENERO' FIELD
        gender = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, gender, id_column, ['R','F'])
        CCS.replace_text(work_df, gender, CCS.gender_sre)
        work_df[gender] = work_df[gender].astype(str).str.strip() # Limpia espacios
        CCS.replace_text(work_df, gender, CCS.gender_sre, ifno=None) # ifno=None para Postgres

        # 'CELULAR' FIELD
        phone = next(headListIter)
        work_df[phone] = work_df[phone].apply(lambda x: CCS.clean_numer(x)) 
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, phone, id_column, ['R'])
        work_df[phone] = work_df[phone].replace('', '1111111111').fillna('1111111111')

        # 'CORREO' new column added on data frame
        mail = next(headListIter)
        work_df[mail] = work_df[mail].fillna(None)

        # 'CIUDAD_REGION' new column added on data frame
        city = next(headListIter)
        if work_df[city].isnull().all():
            work_df[city] = 'Pasto - Nariño'  # Default value if all are NaN
        else:
            work_df[city].fillna('Pasto - Nariño', inplace=True)

        # 'PROFESION' FIELD
        profession = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, profession, id_column, ['R','C','F'])

        # 'CURSO' FIELD
        course = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, course, id_column, ['C','D'])

        # 'MODALIDAD' FIELD
        modality = next(headListIter)
        if work_df[modality].isnull().all():
            work_df[modality] = 'Virtual asincrónica'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, modality, id_column, ['R','C','F'])

        # 'RENOVACION' new column added on data frame
        renew = next(headListIter)
        if work_df[renew].isnull().all():
            work_df[renew] = 'No'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, renew, id_column, ['R','C','F'])

        # 'RESPONSABLE VENTA' FIELD
        seller = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, seller, id_column, ['R','T','F'])

        # 'FECHA DE VENTA' FIELD
        sale_date = next(headListIter)
        standard_date = pd.Timestamp(f'{f_year_int}-{f_month_int:02d}-01')
        
        # 1. Convertir a datetime de forma flexible
        work_df[sale_date] = pd.to_datetime(work_df[sale_date], dayfirst=True, errors='coerce')
        
        # 2. Detectar SOLO las filas que NO coinciden en mes o año (ignorando las vacías de momento)
        mask_wrong_sale = work_df[sale_date].notnull() & ((work_df[sale_date].dt.year != f_year_int) | (work_df[sale_date].dt.month != f_month_int))
        
        # Reemplazar únicamente aquellas fechas que vinieran con un período erróneo
        work_df.loc[mask_wrong_sale, sale_date] = standard_date
        
        # 3. Validar consistencia estructural según los métodos de tu clase Project
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, sale_date, id_column, ['R'])
        
        # 4. Rellenar las celdas que originalmente estaban vacías (NaT) con la fecha por defecto
        work_df[sale_date] = work_df[sale_date].fillna(standard_date)

        # 'VALOR UNITARIO' FIELD
        unit_value = next(headListIter)

        # 'DESCUENTO' FIELD
        discount = next(headListIter)

        # 'PRECIO NETO' FIELD
        net_price = next(headListIter)

        # Nuevas reglas de negocio unificadas para valor_unitario / precio_neto / descuento
        # (sanitización + Escenario 1 o 2 según las columnas presentes en work_df)
        work_df = CCS.apply_pricing_business_rules(
            work_df,
            col_valor_unitario=unit_value,
            col_precio_neto=net_price,
            col_descuento=discount
        )

        # 'MEDIO DE PAGO' FIELD
        payment = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, payment, id_column, ['R','T','F'])

        # 'FECHA DE PAGO' FIELD
        pay_date = next(headListIter)
        
        # 1. Convertir a datetime
        work_df[pay_date] = pd.to_datetime(work_df[pay_date], dayfirst=True, errors='coerce')
        
        # 2. Identificar fechas de pago que no correspondan al período del documento
        mask_wrong_pay = work_df[pay_date].notnull() & ((work_df[pay_date].dt.year != f_year_int) | (work_df[pay_date].dt.month != f_month_int))
        work_df.loc[mask_wrong_pay, pay_date] = pd.NaT
        
        # 3. Rellenar los vacíos o valores erróneos usando la 'FECHA DE VENTA' normalizada
        work_df[pay_date] = work_df[pay_date].fillna(work_df[sale_date])
        
        # 4. Formatear finalmente ambas columnas a string para mantener el estándar visual del Excel
        work_df[sale_date] = work_df[sale_date].dt.strftime('%d/%m/%Y')
        work_df[pay_date] = work_df[pay_date].dt.strftime('%d/%m/%Y')

        # 'ELABORO' FIELD
        maker = next(headListIter)
        work_df[maker] = work_df[maker].astype(str).str.strip().replace(['nan', 'None', 'null'], None)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, maker, id_column, ['R','T','F'])

        # 'PROCEDENCIA' new column added on data frame
        origin = next(headListIter)
        if work_df[origin].isnull().all():
            work_df[origin] = 'Facebook'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, origin, id_column, ['R','C','F'])

        # 'SEGUIMIENTO POST-VENTA' new column added on data frame
        follow_up = next(headListIter)
        if work_df[follow_up].isnull().all():
            work_df[follow_up] = None
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, follow_up, id_column, ['C','F'])

        
        CCS.store_output_files(CCS.cleaned_path, work_df, CCS.rejected_path, wrong_df, file)
        print('*'*50)

# CREATE CONSOLIDATE FILE
CCS.consolidate_work_files_per_year()

# NORMALIZE CATEGORIES IN A SPECIFIC COLUMN
raw_consl_df = pd.read_csv(f'{CCS.info_source_path}/tmp_consolidate.csv')
raw_consl_df.columns = raw_consl_df.columns.str.replace(' ', '_')
NM = NormalMap()

pd.set_option("display.max_rows", None)  # muestra todas las filas

print("*"*50)
print("## ​🤖 NORMALIZANDO CATEGORIAS SEGUN COLUMNA 🦾✍️ ##")
print("*"*50)

print('Numero de categorias antes de normalizar CURSO: ', raw_consl_df['CURSO'].nunique())
raw_consl_df = CCS.normalize_column(raw_consl_df, 'CURSO', NM.courses_map)
print('Numero de categorias despues de normalizar CURSO: ',raw_consl_df['CURSO'].nunique())
print("*" * 50)

print('Numero de categorias antes de normalizar PROFESION: ', raw_consl_df['PROFESION'].nunique())
raw_consl_df = CCS.normalize_column(raw_consl_df, 'PROFESION', NM.professions_map)
print('Numero de categorias despues de normalizar PROFESION: ',raw_consl_df['PROFESION'].nunique())
print("*" * 50)

print("Numero de categorias antes de normalizar ELABORO: ", raw_consl_df['ELABORO'].nunique())
raw_consl_df = CCS.normalize_column(raw_consl_df, 'ELABORO', NM.created_by_map)
print("Numero de categorias despues de normalizar ELABORO: ", raw_consl_df['ELABORO'].nunique())
print("*" * 50)

print("Numero de categorias antes de normalizar RESPONSABLE_VENTA: ", raw_consl_df['RESPONSABLE_VENTA'].nunique())
raw_consl_df = CCS.normalize_column(raw_consl_df, 'RESPONSABLE_VENTA', NM.salesperson_map)
print("Numero de categorias despues de normalizar RESPONSABLE_VENTA: ", raw_consl_df['RESPONSABLE_VENTA'].nunique())
print("*" * 50)

print("Numero de categorias antes de normalizar MEDIO_DE_PAGO: ", raw_consl_df['MEDIO_DE_PAGO'].nunique())
raw_consl_df = CCS.normalize_column(raw_consl_df, 'MEDIO_DE_PAGO', NM.payment_method_map)
print("Numero de categorias despues de normalizar MEDIO_DE_PAGO: ", raw_consl_df['MEDIO_DE_PAGO'].nunique())
print("*" * 50)

print("Numero de categorias antes de normalizar MODALIDAD: ", raw_consl_df['MODALIDAD'].nunique())
raw_consl_df = CCS.normalize_column(raw_consl_df, 'MODALIDAD', NM.modalidad_map)
print("Numero de categorias despues de normalizar MODALIDAD: ", raw_consl_df['MODALIDAD'].nunique())
print("*" * 50)

raw_consl_df.to_csv(f'{CCS.info_source_path}/consolidate_normalized.csv')

path = f'{CCS.info_source_path}/tmp_consolidate.csv'
if os.path.exists(path):
    os.remove(path)
    print('🤖✅​ Archivo temporal normalizado eliminado!')
else:
    print('🤖❌​ No se encontro ningun archivo temporal!')