import pandas as pd


def base_taxtype_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Налоговый орган'].str.contains(
        query_arg, na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table
