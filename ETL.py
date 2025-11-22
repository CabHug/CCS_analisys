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

        ### START DATA CLEANING LOGIC ###
        headListIter = iter(list(work_df.columns))

         # 'NUMERO DE IDENTIFICACION' FIELD
        id_column = next(headListIter)
        work_df[id_column] = work_df[id_column].astype('str').apply(lambda num : CCS.clean_numer(num))
        work_df = work_df.dropna(subset=id_column)
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

        # 'CELULAR' FIELD
        phone = next(headListIter)
        work_df[phone] = work_df[phone].astype(str).str.replace(" ", "", regex=False)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, phone, id_column, ['R'])
        work_df[phone] = work_df[phone].fillna('3000000000')

        # 'CORREO' new column added on data frame
        mail = next(headListIter)
        work_df[mail] = work_df[mail].fillna('null')

        # 'CIUDAD/REGION' new column added on data frame
        city = next(headListIter)
        if (work_df[city]=='null').all():
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
        if (work_df[modality]=='null').all():
            work_df[modality] = 'Virtual asincrónica'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, modality, id_column, ['R','C','F'])

        # 'RENOVACION' new column added on data frame
        renew = next(headListIter)
        if (work_df[renew]=='null').all():
            work_df[renew] = 'No'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, renew, id_column, ['R','C','F'])

        # 'RESPONSABLE VENTA' FIELD
        seller = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, seller, id_column, ['R','T','F'])

        # 'FECHA DE VENTA' new column added on data frame
        sale_date = next(headListIter)
        pay_date = 'FECHA DE PAGO' 
        if (work_df[sale_date]=='null').all():
            work_df[sale_date] = work_df[pay_date]  # Default to pay_date if all are NaN
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, sale_date, id_column, ['R'])
        work_df[sale_date] = pd.to_datetime(work_df[sale_date], format="%d/%m/%Y", errors='coerce')
        work_df[sale_date] = work_df[sale_date].apply(lambda x : x.replace(year=f_year) if pd.notnull(x) and x.year != f_year else x)
        work_df[sale_date] = work_df[sale_date].fillna(pd.Timestamp(f'04/{f_month:02d}/{f_year}'))
        work_df[sale_date] = work_df[sale_date].apply(lambda x : x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

        # 'VALOR UNITARIO' FIELD
        unit_value = next(headListIter)
        work_df[unit_value] = pd.to_numeric(work_df[unit_value], errors='coerce')
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, unit_value, course, ['R'])

        # 'DESCUENTO' new column added on data frame
        discount = next(headListIter)
        if (work_df[discount]=='null').all():
            work_df[discount] = 'Sin descuento'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, discount, id_column, ['R','C','F'])

        # 'PRECIO NETO' new column added on data frame
        net_price = next(headListIter)
        if (work_df[net_price]=='null').all():
            work_df[net_price] = work_df[unit_value]
        else:
            work_df[unit_value] = pd.to_numeric(work_df[unit_value], errors='coerce')
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, net_price, id_column, ['R'])

        # 'MEDIO DE PAGO' FIELD
        payment = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, payment, id_column, ['R','T','F'])

        # 'FECHA DE PAGO' FIELD
        pay_date = next(headListIter)
        work_df[pay_date] = pd.to_datetime(work_df[pay_date], format="%d/%m/%Y", errors='coerce')
        work_df[pay_date] = work_df[pay_date].apply(lambda x : x.replace(year=f_year) if pd.notnull(x) and x.year != f_year else x)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, pay_date, id_column, ['R'])
        work_df[pay_date] = work_df[pay_date].fillna(pd.Timestamp(f'04/{f_month:02d}/{f_year}'))
        work_df[pay_date] = work_df[pay_date].apply(lambda x : x.strftime('%d/%m/%Y') if pd.notnull(x) else x)

        # 'ELABORO' FIELD
        maker = next(headListIter)
        work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, maker, id_column, ['R','T','F'])

        # 'PROCEDENCIA' new column added on data frame
        origin = next(headListIter)
        if (work_df[origin]=='null').all():
            work_df[origin] = 'Facebook'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, origin, id_column, ['R','C','F'])

        # 'SEGUIMIENTO POST-VENTA' new column added on data frame
        follow_up = next(headListIter)
        if (work_df[follow_up]=='null').all():
            work_df[follow_up] = 'null'
        else:
            work_df, wrong_df = CCS.check_if_empty(wrong_df, work_df, follow_up, id_column, ['C','F'])





        print(work_df.head())