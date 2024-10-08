import datetime

import pandas as pd


def datareg_filter(usr_table: pd.DataFrame, query_arg: datetime.datetime) -> pd.DataFrame:
    usr_table['Дата регистрации'] = pd.to_datetime(usr_table['Дата регистрации'], format='%d.%m.%Y')
    date_mask = (usr_table['Дата регистрации'] <= query_arg)
    usr_table = usr_table[date_mask]
    return usr_table
