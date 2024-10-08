import pandas as pd
from filters_table.finance.utils_query_convert import finance_arg_dict, taxmode_arg_dict, finance_flow_str_list
import logging

def fin_2021_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    lst_args = query_arg.split(sep='|')
    args_to_find = ''
    if len(lst_args) == 1:
        try: 
            index_start = finance_flow_str_list.index(lst_args[0])
            args_to_find = '|'.join(finance_flow_str_list[index_start:])
            logging.info(args_to_find)
        except ValueError:
            logging.error('Arg for flow dont find')

    filter_str = usr_table['Оборот за 2021'].str.contains(
        args_to_find, na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def fin_2022_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    lst_args = query_arg.split(sep='|')
    args_to_find = ''
    if len(lst_args) == 1:
        try: 
            index_start = finance_flow_str_list.index(lst_args[0])
            args_to_find = '|'.join(finance_flow_str_list[index_start:])
            logging.info(args_to_find)
        except ValueError:
            logging.error('Arg for flow dont find')
    
    filter_str = usr_table['Оборот за 2022'].str.contains(
        query_arg, na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def fin_2023_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    lst_args = query_arg.split(sep='|')
    args_to_find = ''
    if len(lst_args) == 1:
        try: 
            index_start = finance_flow_str_list.index(lst_args[0])
            args_to_find = '|'.join(finance_flow_str_list[index_start:])
            logging.info(args_to_find)
        except ValueError:
            logging.error('Arg for flow dont find')
    
    filter_str = usr_table['Оборот за 2023'].str.contains(
        query_arg, na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def fin_2024_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    lst_args = query_arg.split(sep='|')
    args_to_find = ''
    if len(lst_args) == 1:
        try: 
            index_start = finance_flow_str_list.index(lst_args[0])
            args_to_find = '|'.join(finance_flow_str_list[index_start:])
            logging.info(args_to_find)
        except ValueError:
            logging.error('Arg for flow dont find')
    
    filter_str = usr_table['Оборот за 2024'].str.contains(
        query_arg, na=False, case=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table


def tax_filter(usr_table: pd.DataFrame, query_arg: str) -> pd.DataFrame:
    filter_str = usr_table['Налоговый режим '].str.contains(
        taxmode_arg_dict[query_arg], na=False)
    usr_table = usr_table[filter_str].reset_index(drop=True)
    return usr_table
