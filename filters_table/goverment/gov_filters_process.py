from telegram import CallbackQuery
import tgUser

import filters_table.goverment.utils_query_convert
import filters_table.goverment.goverment_def_filter
from msg_answer_builder.msg_build_func_collection import send_back_to_menu

async def gov_process(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    if query.data in filters_table.goverment.utils_query_convert.gov_choice_filter_query:
        if query.data == 'CompanyInGov':
            filter_argument = 'Участвовала'
        else:
            filter_argument = 'Не участвовала'
        filter_method_obj = tgUser.FilterMethod(filters_table.goverment.goverment_def_filter.goverment_checker_filter,
                                                filter_argument,
                                                query.data,
                                                "Участие в гос.контрактах")
        cr_user.filter_methods_lst.append(filter_method_obj)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.NO_FILTER
        await send_back_to_menu(query, cr_user)