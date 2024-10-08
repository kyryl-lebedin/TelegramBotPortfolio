import pandas as pd
from filters_table.legal.utils_query_convert import addr_legal_address_dict, legal_address_prolong_dict, \
    legal_cpo_access_dict, legal_license_dict, dir_legal_dict


def legal_address_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Юридический адрес (достоверный/ нет)'].str.contains(
        addr_legal_address_dict[query_arg], na=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def legal_address_prolong_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Пролонгация юр. адреса'].str.contains(
        legal_address_prolong_dict[query_arg], na=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def legal_cpo_access_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Членство, допуск СРО'].str.contains(
        legal_cpo_access_dict[query_arg], na=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def legal_license_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Наличие лицензий'].str.contains(
        legal_license_dict[query_arg], na=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def legal_director_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Руководитель'].str.contains(
        dir_legal_dict[query_arg], na=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table



