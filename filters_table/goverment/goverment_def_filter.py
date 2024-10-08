import pandas as pd

def goverment_checker_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Гос контракты (сумму / не было) '].str.contains(
        "[1-9]+",na=False, regex=True)
    if query_arg == 'CompanyInGov':
        usr_table = usr_table[filter_str].reset_index(drop=True)
    else:
        usr_table = usr_table[~filter_str].reset_index(drop=True)
    return usr_table