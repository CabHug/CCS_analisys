import phonenumbers
import re

### FUNCTION DEFINITION
def clean_numer(number):
    return re.sub(r'\D', '', number)

def find_replace_value(i, id, df, id_column, column):
    value = df.loc[df[id_column] == id, column].dropna().iloc[0]
    df.loc[i, column] = value

# function to find missing information in dataframe, find if any similar data exist to replace in missing one
# parameter action [R(Raplace with similar values), D(drop missing values), F(fill missing values with null), C(To capitalize the text)]
def check_if_empty(wdf, df, column, column2, actions):
    print('*'*50)
    print(f'Data cleaning for {column} column')
    
    # This mask will return al serie bool with values that being empty or NAN
    mask = df[column].apply(lambda x: str(x).strip() == '') | df[column].isna()
    # This serie will contain boolean values, when True has missing data
    id_invalid = df.loc[mask, column2]
    # This serie will cntain boolean values, when True has valid data
    id_valid = df.loc[~mask, column2]
    # This serie will contain values that has a values despite has missing values in another row
    has_value = id_invalid[id_invalid.isin(id_valid)]
    # This serie will contain values that hasn't a value despite has missing values in another row
    has_no_val = id_invalid[~id_invalid.isin(id_valid)]

    for action in  actions:
        # Option when whant to perform replacement with backup
        if action == 'R':
            for i, id in has_value.items():
                find_replace_value(i, id, df, column2, column)
            print("Row that has value: \n", has_value)

        # Option when whant to drop a invalid value
        elif action == 'D':
            for i, id in has_no_val.items():
                wdf = pd.concat([wdf, df.loc[[i]]], ignore_index=True)
                df = df.drop(i, axis=0)
                df = df.reset_index()
            print("Row that hasn't value: \n", has_no_val)

        # Option when whan to perform data filling with null value you can customice it
        elif action == 'F':
            filling = 'null'
            if not has_value.empty:
                print('Please perform a replacement!')
            
            for i, id in has_no_val.items():
                df.loc[i, column] = filling

        # Option to capitalice the text
        elif action == 'C':
            df[column] = df[column].str.capitalize()

        # Option to capitalice everu first letter
        elif action == 'T':
            df[column] = df[column].str.title()
        
        # opciton to uppercase the text
        elif action == 'U':
            df[column] = df[column].str.upper()

        else:
            print("Error! action parameter wrong.")

    return df, wdf

def move_column(df, index, name, n_name=None):
    if n_name is None:
        n_name = name
    values = df.pop(name)
    df.insert(index, n_name, values)

    return df

def remove_column(df, name):
    df.drop(name, axis=1, inplace=True)

def replace_text(df, column, sre, ifno='null'):
    df[column] = df[column].map(sre).fillna(ifno)

def replace_with_othvalue(df, column, sre, ifno='null'):
    df[column] = df[column].map(sre).fillna(ifno)

def phone_validation(number, codigo='CO'):
    try:
        telefono_v = phonenumbers.parse(number, codigo)
        if phonenumbers.is_valid_number(telefono_v):
            return number
        else:
            return 'null'
    except phonenumbers.NumberParseException:
        return 'null'
    
    
