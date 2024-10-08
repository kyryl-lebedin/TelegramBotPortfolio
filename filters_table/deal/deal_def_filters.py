import pandas as pd

from filters_table.deal.utils_query_convert import deal_arg_dict


def deal_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Формат сделки'].str.contains(
        deal_arg_dict[query_arg], na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table
