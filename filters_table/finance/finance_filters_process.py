import types

from telegram import CallbackQuery

import filters_table.finance.utils_query_convert
import filters_table.finance.finance_def_filters
import tgUser
from msg_answer_builder.msg_build_func_collection import send_flow_filter_menu


async def tax_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.finance.utils_query_convert.taxmode_arg_list:
        filter_argument = filters_table.finance.utils_query_convert.taxmode_arg_dict[query.data]
        filter_method_obj = tgUser.FilterMethod(filters_table.finance.finance_def_filters.tax_filter,
                                                filter_argument,
                                                query.data,
                                                "Налоговый режим")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_flow_filter_menu(query, cr_user)


async def flow_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.finance.utils_query_convert.finance_arg_list:
        filter_argument = filters_table.finance.utils_query_convert.finance_arg_dict[query.data]
        # filter_method_obj = None
        if cr_user.filter_stage == tgUser.TgInnUserFilterStage.FLOW_2021:
            if cr_user.has_filter_in_collection("Обороты 2021") != -1:
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2021")].arg = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2021")].arg + \
                    f'|{filter_argument}'
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2021")].arg_readable = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2021")].arg_readable + \
                    f', {filter_argument}'
            else:
                filter_method_obj = tgUser.FilterMethod(filters_table.finance.finance_def_filters.fin_2021_filter,
                                                    filter_argument,
                                                    filter_argument,
                                                    "Обороты 2021")
                cr_user.filter_methods_lst.append(filter_method_obj)

        elif cr_user.filter_stage == tgUser.TgInnUserFilterStage.FLOW_2022:
            if cr_user.has_filter_in_collection("Обороты 2022") != -1:
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2022")].arg = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2022")].arg + \
                    f'|{filter_argument}'
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2022")].arg_readable = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2022")].arg_readable + \
                    f', {filter_argument}'
            else:
                filter_method_obj = tgUser.FilterMethod(filters_table.finance.finance_def_filters.fin_2022_filter,
                                                    filter_argument,
                                                    filter_argument,
                                                    "Обороты 2022")
                cr_user.filter_methods_lst.append(filter_method_obj)

        elif cr_user.filter_stage == tgUser.TgInnUserFilterStage.FLOW_2023:
            if cr_user.has_filter_in_collection("Обороты 2023") != -1:
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2023")].arg = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2023")].arg + \
                    f'|{filter_argument}'
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2023")].arg_readable = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2023")].arg_readable + \
                    f', {filter_argument}'
            else:
                filter_method_obj = tgUser.FilterMethod(filters_table.finance.finance_def_filters.fin_2023_filter,
                                                    filter_argument,
                                                    filter_argument,
                                                    "Обороты 2023")
                cr_user.filter_methods_lst.append(filter_method_obj)
        elif cr_user.filter_stage == tgUser.TgInnUserFilterStage.FLOW_2024:
            if cr_user.has_filter_in_collection("Обороты 2024") != -1:
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2024")].arg = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2024")].arg + \
                    f'|{filter_argument}'
                cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2024")].arg_readable = \
                    cr_user.filter_methods_lst[cr_user.has_filter_in_collection("Обороты 2024")].arg_readable + \
                    f', {filter_argument}'
            else:
                filter_method_obj = tgUser.FilterMethod(filters_table.finance.finance_def_filters.fin_2024_filter,
                                                    filter_argument,
                                                    filter_argument,
                                                    "Обороты 2024")
                cr_user.filter_methods_lst.append(filter_method_obj)

        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_flow_filter_menu(query, cr_user)