import pandas as pd


def base_okved_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Основной ОКВЭД'].str.contains(
        query_arg, na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def additional_okved_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['ОКВЭД (дополнительные)'].str.contains(
        query_arg, na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table