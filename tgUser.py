import enum

import pandas as pd
import datetime

from filters_table.datareg_def_filter import datareg_filter
from filters_table.okved_def_filter import base_okved_filter, additional_okved_filter
from filters_table.taxcontroller_def_filter import base_taxtype_filter
from filters_table.typecompany_def_filter import company_type_filter
from filters_table.deal.deal_def_filters import deal_filter
from filters_table.finance.finance_def_filters import fin_2021_filter, fin_2022_filter, fin_2023_filter, fin_2024_filter, tax_filter
from filters_table.legal.legal_def_filters import legal_address_filter, legal_license_filter, legal_director_filter, legal_cpo_access_filter, legal_address_prolong_filter

import logging

BATCH_SAVE_FILTER = 10

class TgInnUser:
    def __init__(self, username: str, u_id, str_key: str):
        self.username = username
        self.tg_id = u_id
        self.status = TgInnUserStatus.NO_ACTIVE.value
        self.active_key = str_key
        self.query_to_table = FilterQuery()
        self.filter_stage = TgInnUserFilterStage.NO_FILTER
        self.company_list = pd.DataFrame()
        self.index_on_company_list = int(0)
        self.filter_methods_lst = []
        self.save_filter_list = []
        self.cr_pos_save_filter_list = int(0)
    
    def has_filter_in_collection(self, readable_filter_type: str):
        for i, data_filter in enumerate(self.filter_methods_lst):
            if data_filter.filter_method_readable == readable_filter_type:
                return i
        return -1

    def add_region_to_user_filter(self, query_data):
        if query_data in self.query_to_table.region:
            self.query_to_table.region.remove(query_data)
        else:
            self.query_to_table.region.add(query_data)

    def load_filter_methods(self, filter_methods: list):
        for filter_method in filter_methods:
            if filter_method[0] == 'region':
                self.query_to_table.region.add(filter_method[2])
            else:
                method = filter_mapper.get(filter_method[0])
                
                # notice, arg is always string from db, if filter takes non str arg, it should be converted
                object_method = FilterMethod(method, filter_method[3], filter_method[2], filter_method[1])
                self.filter_methods_lst.append(object_method)
        
    def get_batch_of_company(self) -> pd.DataFrame:
        length_of_batch = 5
        end_index = 0
        if self.index_on_company_list + length_of_batch >= len(self.company_list):
            end_index = len(self.company_list)
        else:
            end_index = self.index_on_company_list + length_of_batch
        company_batch = self.company_list.iloc[self.index_on_company_list:end_index]
        self.index_on_company_list = self.index_on_company_list + 5
        return company_batch
    
    def _get_ssch_val(self, data: str) -> bool:
        start_val_post = data.rfind(' ')
        val = data[start_val_post:]
        if data == '' or data == 'Нет':
            return True
        
        try:
            int_val = int(val)
            if int_val == 0:
                return True
        except ValueError:
            return True
        
        return False
    
    def _check_cashflow_reg_act(self, year_reg: int, flow_year_val: str) -> bool:
        start_val_post = flow_year_val.rfind(' ')
        val_to_check = flow_year_val[start_val_post:]
        try:
            year_int_val = int(val_to_check)
            if year_int_val >= year_reg:
                return False
            else:
                return True
        except ValueError:
            return True
        
    def _check_getcash_by_reg_act(self, year_reg: int, get_cash_val: str) -> str:
        res_str = ""
        get_cash_arr = get_cash_val.split(sep='\n')
        for cash_val in get_cash_arr:
            pos_to_slice = cash_val.find(' ')
            if (pos_to_slice != -1):
                try:
                    val_to_parse = int(cash_val[:pos_to_slice])
                    if val_to_parse >= year_reg:
                        res_str = res_str + cash_val + '\n'
                except ValueError:
                    pass
        return res_str

    async def build_msg_from_batch_of_company(self, company_table: pd.DataFrame) -> list:
        # company_table = self.get_batch_of_company()
        msg_list = []
        clmn_list = company_table.columns.to_list()
        for rows in company_table.iterrows():
            year_of_reg = datetime.datetime.strptime(str(rows[1]['Дата регистрации']), "%d.%m.%Y").year
            msg_with_company_info = 'Снаб №:' + str(rows[1]['Снаб №']) + "\n"
            for i in range(3, 23):
                if clmn_list[i].find('Банки') != -1 and (rows[1][clmn_list[i]] == '' or rows[1][clmn_list[i]].find('Без счетов') != -1):
                    continue
                if clmn_list[i].find('Оборот') != -1 and self._check_cashflow_reg_act(year_of_reg, clmn_list[i]):
                    continue
                if clmn_list[i] == 'ССЧ' and  self._get_ssch_val(rows[1][clmn_list[i]]):
                    continue
                if clmn_list[i] == 'Комментарий' and rows[1][clmn_list[i]] == '':
                    continue
                if clmn_list[i].find('База 1с') != -1 and rows[1][clmn_list[i]] == '':
                    continue
                if clmn_list[i].find('Первичка') != -1 and rows[1][clmn_list[i]] == '':
                    continue
                if clmn_list[i] == 'out':
                    continue
                if clmn_list[i] == 'Дата регистрации':
                    if type(rows[1][clmn_list[i]]) is str:
                        msg_with_company_info = msg_with_company_info + clmn_list[i] + ': ' + str(
                            rows[1][clmn_list[i]]) + "\n"
                    else:
                        msg_with_company_info = msg_with_company_info + clmn_list[i] + ': ' + str(
                            rows[1][clmn_list[i]].strftime("%d.%m.%Y")) + "\n"
                    continue
                if clmn_list[i] == 'Выручка':
                    cash_act_str = self._check_getcash_by_reg_act(year_of_reg, str(rows[1][clmn_list[i]]))
                    if cash_act_str != "":
                        msg_with_company_info = msg_with_company_info + clmn_list[i] + ':\n'
                    # msg_with_company_info = msg_with_company_info + str(rows[1][clmn_list[i]])
                        msg_with_company_info = msg_with_company_info + cash_act_str
                    continue

                msg_with_company_info = msg_with_company_info + clmn_list[i] + ': ' + str(rows[1][clmn_list[i]]) + "\n"

            str_gos = str(rows[1]['Гос контракты (сумму / не было) '])
            if int(str_gos.split()[4]) != 0 or int(str_gos.split()[15]) != 0:  # - 4: cnt postashik gos 15: cnt zakp gos
                msg_with_company_info = msg_with_company_info + 'Гос контракты: ' + \
                                        str(rows[1]['Гос контракты (сумму / не было) ']) + "\n"

            if str(rows[1]['Пролонгация юр. адреса']).find('Без пролонгации') != -1:
                msg_with_company_info = msg_with_company_info + 'Пролонгация юр. адреса: ' + 'Нет' + "\n"
            elif str(rows[1]['Пролонгация юр. адреса']).find('С пролонгацией') != -1:
                msg_with_company_info = msg_with_company_info + 'Пролонгация юр. адреса: ' + 'Да' + "\n"
            
            if str(rows[1]['Членство, допуск СРО']).find('Без СРО') == -1:
                msg_with_company_info = msg_with_company_info + 'Членство, допуск СРО: ' + \
                                        str(rows[1]['Членство, допуск СРО']) + "\n"
                
            if str(rows[1]['Наличие лицензий']).find('Без лицензий') == -1:
                msg_with_company_info = msg_with_company_info + 'Наличие лицензий: ' + \
                                        str(rows[1]['Наличие лицензий']) + "\n"
            
            msg_with_company_info = msg_with_company_info + 'Цена (Договорная): ' + \
                                    str(rows[1]['out'])

            msg_list.append(msg_with_company_info)
        return msg_list

    async def clear_params(self) -> None:
        self.filter_methods_lst.clear()
        self.company_list = pd.DataFrame()
        self.index_on_company_list = int(0)
        self.query_to_table.region.clear()
        self.cr_pos_save_filter_list = int(0)
        self.filter_stage = TgInnUserFilterStage.NO_FILTER

    async def slice_save_filters_to_send(self, mode) -> list:
        filter_slice_list = []
        logging.info(self.save_filter_list)
        if mode == FilterSliceMode.NEXT_MODE:
            logging.info(f"filter start {self.cr_pos_save_filter_list} End {self.cr_pos_save_filter_list + BATCH_SAVE_FILTER}")
            filter_slice_list = self.save_filter_list[
                self.cr_pos_save_filter_list:self.cr_pos_save_filter_list + BATCH_SAVE_FILTER
            ]
            if self.cr_pos_save_filter_list + BATCH_SAVE_FILTER < len(self.save_filter_list):
                self.cr_pos_save_filter_list = self.cr_pos_save_filter_list + BATCH_SAVE_FILTER
        elif mode == FilterSliceMode.PREV_MODE:
            if self.cr_pos_save_filter_list - BATCH_SAVE_FILTER < 0:
                self.cr_pos_save_filter_list = 0
            else:
                self.cr_pos_save_filter_list = self.cr_pos_save_filter_list - BATCH_SAVE_FILTER
            logging.info(f"filter start {self.cr_pos_save_filter_list} End {self.cr_pos_save_filter_list + BATCH_SAVE_FILTER}")
            filter_slice_list = self.save_filter_list[
                self.cr_pos_save_filter_list:self.cr_pos_save_filter_list + BATCH_SAVE_FILTER
            ]
        return filter_slice_list


class FilterQuery:
    def __init__(self):
        self.region = set()


class FilterMethod:
    def __init__(self, method, arg_readable, arg_raw, read_format_method):
        self.arg = arg_raw
        self.arg_readable = arg_readable
        self.filter_method = method
        self.filter_method_readable = read_format_method


class TgInnUserStatus(enum.Flag):
    NO_ACTIVE = 0
    DEAL_TYPE_STAGE = 1
    ORG_DATA_STAGE = 2
    IN_DATA_STAGE = 3
    OUT_DATA_STAGE = 4
    COMPANY_SHOW_STAGE = 5
    INN_DIRECT_STAGE = 6
    BASE_OKVED_STAGE = 7
    ADD_OKVED_STAGE = 8
    DATE_REG_STAGE = 9
    TAX_CONTROLLER_STAGE = 10
    COMPANY_TYPE_STAGE = 11
    SAVE_FILTER_STAGE = 12
    CHOOSE_FILTER_STAGE = 13
    FIND_SAVE_FILTER_STAGE = 14


class TgInnUserFilterStage(enum.Flag):
    NO_FILTER = 0
    ADDR_LEGAL_FILTER = 1
    ADDR_PROLONG_FILTER = 2
    CPO_LEGAL_FILTER = 3
    LICENSE_LEGAL_FILTER = 4
    DIR_LEGAL_FILTER = 5
    FLOW_2021 = 6
    FLOW_2022 = 7
    FLOW_2023 = 8
    FLOW_2024 = 9
    TAX_MODE = 10


class FilterSliceMode(enum.Flag):
    NEXT_MODE = 0
    PREV_MODE = 1

filter_mapper = {'datareg_filter': datareg_filter, 'base_okved_filter': base_okved_filter, 
                 'additional_okved_filter':additional_okved_filter, 'base_taxtype_filter': base_taxtype_filter, 
                 'company_type_filter': company_type_filter, 'deal_filter': deal_filter, 
                 'fin_2021_filter': fin_2021_filter, 'fin_2022_filter': fin_2022_filter, 
                 'fin_2023_filter': fin_2023_filter, 'fin_2024_filter': fin_2024_filter, 
                 'tax_filter': tax_filter, 'legal_address_filter': legal_address_filter, 
                 'legal_license_filter': legal_license_filter, 'legal_director_filter': legal_director_filter, 
                 'legal_cpo_access_filter': legal_cpo_access_filter, 'legal_address_prolong_filter': legal_address_prolong_filter}

