import asyncio
import datetime
import logging

import pandas as pd
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

import filters_table.datareg_def_filter
import filters_table.deal.deal_filters_process
import filters_table.deal.utils_query_convert
import filters_table.finance.finance_filters_process
import filters_table.finance.utils_query_convert
import filters_table.legal.legal_filter_usr_process
import filters_table.legal.utils_query_convert
import filters_table.okved_def_filter
import filters_table.taxcontroller_def_filter
import filters_table.typecompany_def_filter
import filters_table.goverment.utils_query_convert
import filters_table.goverment.gov_filters_process
import google_sheet_custom_processor
import inlineKeyBoardCollections
import msg_answer_builder.msg_build_func_collection as bot_answer
from UserManager import UserManager
from postgres.postgres import DatabaseManager, DB_URL, LicenseKey, UserFilters, FiltersMethods
from tgUser import TgInnUserStatus, TgInnUserFilterStage, FilterMethod, FilterQuery, FilterSliceMode

logging.basicConfig(
    filename='logs/bot_log.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def parse_query_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    index_usr = await user_manager.check_user_in_list_query(update)
    current_user = user_manager.user_collection[index_usr]

    if query.data == 'RegChoice':
        await bot_answer.send_choice_region_menu(query)
    elif query.data == 'BackToMain':
        await bot_answer.send_back_to_menu(query, current_user)
    elif query.data == 'LegalMenu':
        await bot_answer.send_legal_filter_menu(query, current_user)
    elif query.data == 'CashFlow':
        await bot_answer.send_flow_filter_menu(query, current_user)
    elif query.data == 'DealMenu':
        await bot_answer.send_deal_filter_menu(query, current_user)
    elif query.data == 'GovermentChoicer':
        await bot_answer.process_gov_controller_request(query, current_user)
    elif query.data == 'SaveFilters':
         await bot_answer.process_save_filters_request(update, context, current_user)
    elif query.data == 'MyFilters':
        current_user.save_filter_list = user_manager.db_manager.get_all_user_filters(current_user) # ОК
        slice_save_filter_lst = await current_user.slice_save_filters_to_send(FilterSliceMode.NEXT_MODE)
        logging.info(slice_save_filter_lst)
        await bot_answer.send_my_filters_menu(update, context, current_user, slice_save_filter_lst, query)
    elif query.data == 'EraseFilters':
        await current_user.clear_params()
        await bot_answer.send_back_to_menu(query, current_user)
    elif query.data == 'NextBatchFilters':
        slice_save_filter_lst = await current_user.slice_save_filters_to_send(FilterSliceMode.NEXT_MODE)
        logging.info(f'Next batch {slice_save_filter_lst}')
        await bot_answer.send_my_filters_menu(update, context, current_user, slice_save_filter_lst, query)
    elif query.data == 'PreviusBatchFilters':
        slice_save_filter_lst = await current_user.slice_save_filters_to_send(FilterSliceMode.PREV_MODE)
        logging.info(f'Next batch {slice_save_filter_lst}')
        await bot_answer.send_my_filters_menu(update, context, current_user, slice_save_filter_lst, query)
    elif query.data == 'FindSaveFilterByName':
        await bot_answer.process_find_by_name_save_filters_request(update, context, current_user)
    elif query.data == 'GetComp':
        await bot_answer.process_get_company_req(query, current_user)
    elif query.data == 'GetCompFive':
        await bot_answer.process_get_batch_of_company(update, context, current_user)
    elif query.data == 'LoadFilters':
        filters = user_manager.db_manager.load_user_filters(filters_id = current_user.get_filter[0])
        await current_user.clear_params()
        current_user.load_filter_methods(filters)
        await bot_answer.send_back_to_menu(query, current_user)
    elif query.data == 'DeleteFilters':
        user_manager.db_manager.delete_user_filter(filter_id=current_user.get_filter[0])
        await bot_answer.send_back_to_menu(query, current_user)
    elif query.data in filters_table.deal.utils_query_convert.deal_choice_filter_query:
        await filters_table.deal.deal_filters_process.tax_process(query, current_user)
    elif query.data in filters_table.finance.utils_query_convert.finance_choice_filter_query:
        await bot_answer.process_flow_filters(query, current_user)
    elif query.data in filters_table.goverment.utils_query_convert.gov_choice_filter_query:
        await filters_table.goverment.gov_filters_process.gov_process(query, current_user)
    elif current_user.filter_stage == TgInnUserFilterStage.FLOW_2021 or \
            current_user.filter_stage == TgInnUserFilterStage.FLOW_2022 or \
            current_user.filter_stage == TgInnUserFilterStage.FLOW_2023 or \
            current_user.filter_stage == TgInnUserFilterStage.FLOW_2024:
        await filters_table.finance.finance_filters_process.flow_process(query, current_user)
    elif current_user.filter_stage == TgInnUserFilterStage.TAX_MODE:
        await filters_table.finance.finance_filters_process.tax_process(query, current_user)

    elif query.data in filters_table.legal.utils_query_convert.legal_choice_filter_query:
        await bot_answer.process_legal_filters(query, current_user)
    elif current_user.filter_stage == TgInnUserFilterStage.ADDR_LEGAL_FILTER:
        await filters_table.legal.legal_filter_usr_process.legal_address_process(query, current_user)
    elif current_user.filter_stage == TgInnUserFilterStage.ADDR_PROLONG_FILTER:
        await filters_table.legal.legal_filter_usr_process.legal_address_prolong_process(query, current_user)
    elif current_user.filter_stage == TgInnUserFilterStage.CPO_LEGAL_FILTER:
        await filters_table.legal.legal_filter_usr_process.legal_cpo_process(query, current_user)
    elif current_user.filter_stage == TgInnUserFilterStage.LICENSE_LEGAL_FILTER:
        await filters_table.legal.legal_filter_usr_process.legal_license_process(query, current_user)
    elif current_user.filter_stage == TgInnUserFilterStage.DIR_LEGAL_FILTER:
        await filters_table.legal.legal_filter_usr_process.legal_dir_process(query, current_user)
    elif query.data == 'MscReg' or query.data == 'SpbReg' or query.data == 'FarReg':
        # user_manager.user_collection[index_usr].query_to_table.region = query.data
        logger = logging.getLogger(__name__)
        logger.info(f'Start set region by {vars(current_user)}')
        current_user.add_region_to_user_filter(query.data)
        await bot_answer.send_back_to_menu(query, current_user)
        logger.info(f'End set region by {vars(current_user)}')
    elif query.data == 'InnRequest':
        await bot_answer.process_direct_inn_request(update, context, current_user)
    elif query.data == 'BaseOkv':
        await bot_answer.process_base_okved_request(update, context, current_user)
    elif query.data == 'AddOkv':
        await bot_answer.process_additional_okved_request(update, context, current_user)
    elif query.data == 'DateReg':
        await bot_answer.process_reg_time_request(update, context, current_user)
    elif query.data == 'TaxController':
        await bot_answer.process_tax_controller_request(update, context, current_user)
    elif query.data == 'CompanyType':
        await bot_answer.process_company_type_request(update, context, current_user)
    elif current_user.status == TgInnUserStatus.CHOOSE_FILTER_STAGE.value:
        current_user.get_filter = query.data.split()
        await bot_answer.process_filter_delete_load(update, context, current_user)


async def process_text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    index_usr = await user_manager.check_user_in_list(update)
    current_user = user_manager.user_collection[index_usr]

    logger = logging.getLogger(__name__)
    logger.info(f'Client params {vars(current_user)}')

    if current_user.status == TgInnUserStatus.INN_DIRECT_STAGE.value:
        try:
            inn_args = [str(int(vals)) for vals in update.message.text.split('\n') if vals != '']
            logging.info(f'Inn args {inn_args}')
        except ValueError:
            test_answer_wrong_inn = "Введенный ИНН ошибочен. Попробуйте еще раз"
            reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=test_answer_wrong_inn,
                                           reply_markup=reply_markup)
            return

        full_region_query = FilterQuery()
        full_region_query.region = frozenset(['MscReg', 'SpbReg', 'FarReg'])
        inn_value = '|'.join(inn_args)
        logging.info(f'Inn args {inn_value}')
        current_user.company_list = google_sheet_custom_processor.get_company_by_direct_inn_request(
            full_region_query,
            inn_value
        )
        if len(current_user.company_list) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Компания с таким ИНН не найдена.')
        else:
            msg_to_send = await current_user.build_msg_from_batch_of_company(current_user.company_list)
            for msg in msg_to_send:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
                await asyncio.sleep(1)

        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        current_user.index_on_company_list = int(0)
        current_user.company_list = pd.DataFrame(None)
        await bot_answer.send_back_to_menu_msg(update, context, current_user)
        
    elif current_user.status == TgInnUserStatus.SAVE_FILTER_STAGE.value:
        try:
            filter_name = update.message.text
        except ValueError:
            # add name restrictions if needed
            test_answer_wrong_inn = "Введенное название ошибочно. Попробуйте еще раз"
            reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=test_answer_wrong_inn,
                                           reply_markup=reply_markup)
            return

        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        user_manager.save_users_filters(filter_name, current_user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Фильтр '{filter_name}' успешно сохранен.")
        await bot_answer.send_back_to_menu_msg(update, context, current_user)

    elif current_user.status == TgInnUserStatus.FIND_SAVE_FILTER_STAGE.value:
        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
        current_user.save_filter_list = user_manager.db_manager.get_user_filters_by_name(current_user, update.message.text)
        current_user.cr_pos_save_filter_list = 0
        slice_save_filter_lst = await current_user.slice_save_filters_to_send(FilterSliceMode.NEXT_MODE)
        logging.info(slice_save_filter_lst)
        await bot_answer.send_my_filters_menu(update, context, current_user, slice_save_filter_lst)
    elif current_user.status == TgInnUserStatus.BASE_OKVED_STAGE.value:
        args_parse = update.message.text.split(sep=';')
        filter_arg = '|'.join(args_parse)
        filter_method_obj = FilterMethod(filters_table.okved_def_filter.base_okved_filter,
                                                update.message.text,
                                                filter_arg,
                                                "Осн. ОКВЭД")
        current_user.filter_methods_lst.append(filter_method_obj)
        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        await bot_answer.send_back_to_menu_msg(update, context, current_user)
    elif current_user.status == TgInnUserStatus.ADD_OKVED_STAGE.value:
        args_parse = update.message.text.split(sep=';')
        filter_arg = '|'.join(args_parse)
        filter_method_obj = FilterMethod(filters_table.okved_def_filter.additional_okved_filter,
                                                update.message.text,
                                                filter_arg,
                                                "Доп. ОКВЭД")
        current_user.filter_methods_lst.append(filter_method_obj)
        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        await bot_answer.send_back_to_menu_msg(update, context, current_user)
    elif current_user.status == TgInnUserStatus.DATE_REG_STAGE.value:
        usr_date_msg = update.message.text
        try:
            usr_start_date_event = datetime.datetime.strptime(usr_date_msg, "%d.%m.%Y")
        except ValueError:
            msg_to_send = "Неверный формат даты. Формат даты: %D.%M.%YYYY. Примеры: 10.04.2023, 02.11.2022."
            reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=msg_to_send,
                                           reply_markup=reply_markup)
            return
        filter_method_obj = FilterMethod(filters_table.datareg_def_filter.datareg_filter,
                                         str(usr_start_date_event.strftime("%d.%m.%Y")),
                                         usr_start_date_event,
                                         "Фильтр даты регистрации компании до даты")
        current_user.filter_methods_lst.append(filter_method_obj)
        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        await bot_answer.send_back_to_menu_msg(update, context, current_user)
    elif current_user.status == TgInnUserStatus.TAX_CONTROLLER_STAGE.value:
        filter_method_obj = FilterMethod(filters_table.taxcontroller_def_filter.base_taxtype_filter,
                                         update.message.text,
                                         update.message.text,
                                         "Налоговый орган: ")
        current_user.filter_methods_lst.append(filter_method_obj)
        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        await bot_answer.send_back_to_menu_msg(update, context, current_user)
    elif current_user.status == TgInnUserStatus.COMPANY_TYPE_STAGE.value:
        filter_method_obj = FilterMethod(filters_table.typecompany_def_filter.company_type_filter,
                                         update.message.text,
                                         update.message.text,
                                         "Тип компании: ")
        current_user.filter_methods_lst.append(filter_method_obj)
        current_user.status = TgInnUserStatus.NO_ACTIVE.value
        await bot_answer.send_back_to_menu_msg(update, context, current_user)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = await user_manager.check_user_in_list(update)
    if res != -1:
        current_user = user_manager.user_collection[res]
        await current_user.clear_params()
        test_answer_begin = "Доброго дня! Данный бот помогает выгрузить компании из доступных в вашей базе данных!\n" \
                            "Выберите регион, настройте фильтры или сделайте прямой запрос по ИНН!"
        reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_base)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=test_answer_begin,
                                       reply_markup=reply_markup)
    else:
        test_answer_restrict = "Доступ к боту вам запрещен!"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=test_answer_restrict)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = await user_manager.check_licence_from_user(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{res}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите /start для начала работы.")


if __name__ == '__main__':
    user_manager = UserManager()
    
    


    application = ApplicationBuilder().token('token').build()


    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)
    application.add_handler(CallbackQueryHandler(parse_query_request))
    application.add_handler(start_handler)
    application.add_handler(register_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_text_msg))


    application.run_polling()
