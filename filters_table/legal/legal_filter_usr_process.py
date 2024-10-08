import types

from telegram import CallbackQuery

import filters_table.legal.utils_query_convert
from filters_table.legal.legal_def_filters import legal_address_filter
import tgUser
from msg_answer_builder.msg_build_func_collection import send_legal_filter_menu


async def legal_address_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.legal.utils_query_convert.addr_legal_address_lst:
        filter_argument = filters_table.legal.utils_query_convert.addr_legal_address_dict[query.data]
        filter_method_obj = tgUser.FilterMethod(filters_table.legal.legal_def_filters.legal_address_filter,
                                                filter_argument,
                                                query.data,
                                                "Адрес/Достоверенность")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_legal_filter_menu(query, cr_user)


async def legal_address_prolong_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.legal.utils_query_convert.legal_address_prolong_lst:
        filter_argument = filters_table.legal.utils_query_convert.legal_address_prolong_dict[query.data]
        filter_method_obj = tgUser.FilterMethod(filters_table.legal.legal_def_filters.legal_address_prolong_filter,
                                                filter_argument,
                                                query.data,
                                                "Адрес/Пролонгация")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_legal_filter_menu(query, cr_user)


async def legal_cpo_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.legal.utils_query_convert.legal_cpo_access_lst:
        filter_argument = filters_table.legal.utils_query_convert.legal_cpo_access_dict[query.data]
        filter_method_obj = tgUser.FilterMethod(filters_table.legal.legal_def_filters.legal_cpo_access_filter,
                                                filter_argument,
                                                query.data,
                                                "Членство допуск CPO")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_legal_filter_menu(query, cr_user)


async def legal_license_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.legal.utils_query_convert.legal_license_lst:
        filter_argument = filters_table.legal.utils_query_convert.legal_license_dict[query.data]
        filter_method_obj = tgUser.FilterMethod(filters_table.legal.legal_def_filters.legal_license_filter,
                                                filter_argument,
                                                query.data,
                                                "Наличие лицензий")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_legal_filter_menu(query, cr_user)


async def legal_dir_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.legal.utils_query_convert.dir_legal_lst:
        filter_argument = filters_table.legal.utils_query_convert.dir_legal_dict[query.data]
        filter_method_obj = tgUser.FilterMethod(filters_table.legal.legal_def_filters.legal_director_filter,
                                                filter_argument,
                                                query.data,
                                                "Руководитель")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_legal_filter_menu(query, cr_user)
