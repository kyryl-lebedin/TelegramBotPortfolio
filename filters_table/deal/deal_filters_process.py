import types

from telegram import CallbackQuery

import filters_table.deal.utils_query_convert
import filters_table.deal.deal_def_filters
import tgUser
from msg_answer_builder.msg_build_func_collection import send_back_to_menu


async def tax_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.deal.utils_query_convert.deal_choice_filter_query:
        filter_argument = filters_table.deal.utils_query_convert.deal_arg_dict[query.data]
        filter_method_obj = tgUser.FilterMethod(filters_table.deal.deal_def_filters.deal_filter,
                                                filter_argument,
                                                query.data,
                                                "Формат сделки")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_back_to_menu(query, cr_user)