import asyncio

from telegram import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton, Update
from telegram.ext import ContextTypes

import filters_table.legal.inlinaLegalKeyboard
import filters_table.finance.inlineFinanceKeyboard
import tgUser
import inlineKeyBoardCollections
from google_sheet_custom_processor import build_data_from_google_sheet


async def send_back_to_menu(query: CallbackQuery, current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.NO_ACTIVE.value
    current_user.cr_pos_save_filter_list = 0
    current_user.get_filter = 0
    test_answer_begin = "Доброго дня! Данный бот помогает выгрузить компании из доступных в вашей базе данных!\n" \
                        "Выберите регион, настройте фильтры или сделайте прямой запрос по ИНН!"
    if len(current_user.query_to_table.region) != 0:
        region_lst = []
        for region in current_user.query_to_table.region:
            region_lst.append(inlineKeyBoardCollections.keyboard_regions_dict[region])
        region_str = ";".join(region_lst)
        test_answer_begin = test_answer_begin + '\n' + f'Ваши регионы работы: ' + region_str

    test_answer_begin = build_filter_msg_info(current_user, test_answer_begin)

    if len(current_user.query_to_table.region) != 0 or len(current_user.filter_methods_lst) != 0:
        tmp_keyboard = inlineKeyBoardCollections.keyboard_base_filters_on
    else:
        tmp_keyboard = inlineKeyBoardCollections.keyboard_base

    reply_markup = InlineKeyboardMarkup(tmp_keyboard)
    await query.edit_message_text(text=test_answer_begin)
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def send_back_to_menu_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.NO_ACTIVE.value

    test_answer_begin = "Доброго дня! Данный бот помогает выгрузить компании из доступных в вашей базе данных!\n" \
                        "Выберите регион, настройте фильтры или сделайте прямой запрос по ИНН!"
    if len(current_user.query_to_table.region) != 0:
        region_lst = []
        for region in current_user.query_to_table.region:
            region_lst.append(inlineKeyBoardCollections.keyboard_regions_dict[region])
        region_str = ";".join(region_lst)
        test_answer_begin = test_answer_begin + '\n' + f'Ваши регионы работы: ' + region_str

    test_answer_begin = build_filter_msg_info(current_user, test_answer_begin)

    if len(current_user.query_to_table.region) != 0 or len(current_user.filter_methods_lst) != 0:
        tmp_keyboard = inlineKeyBoardCollections.keyboard_base_filters_on
    else:
        tmp_keyboard = inlineKeyBoardCollections.keyboard_base

    reply_markup = InlineKeyboardMarkup(tmp_keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=test_answer_begin, reply_markup=reply_markup)


async def process_company_type_request(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.COMPANY_TYPE_STAGE.value
    test_answer = "По какому типу ищите компанию? (ООО, АО и т.д)"
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=test_answer,
                                   reply_markup=reply_markup)

async def process_filter_delete_load(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                     current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.NO_ACTIVE.value
    test_answer = f"{current_user.get_filter[1]}"
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_load_delete_filters + inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=test_answer,
                                   reply_markup=reply_markup)


async def process_tax_controller_request(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.TAX_CONTROLLER_STAGE.value
    test_answer = "Введите запрос по фильтру для налогового органа:"
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=test_answer,
                                   reply_markup=reply_markup)

async def process_reg_time_request(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.DATE_REG_STAGE.value
    test_answer = "Введите дату регистрации организации.\n Поиск будет происходить по всем организациям старше этой даты.\n" \
                  "Формат даты: %D.%M.%YYYY. Примеры: 10.04.2023, 02.11.2022."
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=test_answer,
                                   reply_markup=reply_markup)


async def process_base_okved_request(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.BASE_OKVED_STAGE.value
    test_answer = "Введите слово или фразу для поиска по Осн. ОКВЭД"
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=test_answer,
                                   reply_markup=reply_markup)


async def process_additional_okved_request(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.ADD_OKVED_STAGE.value
    test_answer = "Введите слово или фразу для поиска по Дополнительными ОКВЭД"
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=test_answer,
                                   reply_markup=reply_markup)


async def process_direct_inn_request(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     current_user: tgUser.TgInnUser):
    if current_user.query_to_table.region == "":
        test_answer_not_inn = "Для прямого запроса по инн необходимо выбрать регион" \
                              "по которому вы работайте!!!"
        reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_base)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=test_answer_not_inn,
                                       reply_markup=reply_markup)
    else:
        current_user.status = tgUser.TgInnUserStatus.INN_DIRECT_STAGE.value
        test_answer_not_inn = "Введите ИНН, который вас интересует"
        reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=test_answer_not_inn,
                                       reply_markup=reply_markup)
        
async def process_save_filters_request(update: Update, context: ContextTypes.DEFAULT_TYPE, current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.SAVE_FILTER_STAGE.value
    test_answer = "Выберите название для вашего фильтра"   
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=test_answer, reply_markup=reply_markup)

async def process_find_by_name_save_filters_request(update: Update, context: ContextTypes.DEFAULT_TYPE, current_user: tgUser.TgInnUser):
    current_user.status = tgUser.TgInnUserStatus.FIND_SAVE_FILTER_STAGE.value
    test_answer = "Введите название сохраннего набора фильтров: "   
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=test_answer, reply_markup=reply_markup)

# send_back_to_menu
async def send_choice_region_menu(query: CallbackQuery):
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_regions)
    await query.edit_message_text(text="Выберите регион, по которому будет проходить поиск")
    await query.edit_message_reply_markup(reply_markup=reply_markup)

async def send_my_filters_menu(update, context, cr_user: tgUser.TgInnUser, filters: list, query: CallbackQuery = None):
    if filters:
        test_answer = "Выберите фильтр: "
        
        buttons = [[InlineKeyboardButton(text=f'{filter[0]} - {filter[1]}', callback_data=f'{filter[0]} {filter[1]}')] for filter in filters]
        buttons.insert(0, inlineKeyBoardCollections.keyboard_find_filter_by_name[0])
        buttons.append(inlineKeyBoardCollections.keyboard_save_filter_navi[0])
        buttons.append(inlineKeyBoardCollections.keyboard_save_filter_navi[1])
        buttons.append(inlineKeyBoardCollections.keyboard_back_to_menu_from_filter[0])
        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        cr_user.status = tgUser.TgInnUserStatus.CHOOSE_FILTER_STAGE.value
        if query is not None:
            await query.edit_message_text(text=test_answer)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=test_answer,
                                           reply_markup=reply_markup)
    else:
        test_answer_wrong_inn = "У вас нет сохраненных фильтров"
        reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_back_to_menu)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=test_answer_wrong_inn,
                                           reply_markup=reply_markup)
        return



async def send_legal_filter_menu(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    test_answer_begin = "Выберите фильтр: "
    test_answer_begin = build_filter_msg_info(cr_user, test_answer_begin)
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_legal_filters)
    await query.edit_message_text(text=test_answer_begin)
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def send_flow_filter_menu(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    test_answer_begin = "Выберите фильтр: "
    test_answer_begin = build_filter_msg_info(cr_user, test_answer_begin)
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_cashflow_filters)
    await query.edit_message_text(text=test_answer_begin)
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def send_deal_filter_menu(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    test_answer_begin = "Выберите фильтр: "
    test_answer_begin = build_filter_msg_info(cr_user, test_answer_begin)
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_deal_filters)
    await query.edit_message_text(text=test_answer_begin)
    await query.edit_message_reply_markup(reply_markup=reply_markup)

async def process_gov_controller_request(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_company_in_gov_filters)
    await query.edit_message_text(text="Укажите, компания участвовала в гос.контрактах?")
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def process_flow_filters(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    flow_conv_dict = {
        'flow2021': tgUser.TgInnUserFilterStage.FLOW_2021,
        'flow2022': tgUser.TgInnUserFilterStage.FLOW_2022,
        'flow2023': tgUser.TgInnUserFilterStage.FLOW_2023,
        'flow2024': tgUser.TgInnUserFilterStage.FLOW_2024
    }
    if flow_conv_dict.get(query.data, None) is None:
        test_answer_begin = 'Выберите тип налого обложения'
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.TAX_MODE
        keyboard_raw = filters_table.finance.inlineFinanceKeyboard.keyword_tax_mode.copy()
    else:
        cr_user.filter_stage = flow_conv_dict[query.data]
        test_answer_begin = 'Выберите размер оборота: '
        keyboard_raw = filters_table.finance.inlineFinanceKeyboard.keyboard_flow_size.copy()

    keyboard_raw.append(
        [InlineKeyboardButton("⬅ Назад ⬅", callback_data="CashFlow")]
    )
    reply_markup = InlineKeyboardMarkup(keyboard_raw)
    await query.edit_message_text(text=test_answer_begin)
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def process_legal_filters(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    test_answer_begin = ''
    reply_markup = None
    if query.data == 'checkAddr':
        test_answer_begin = 'Выберите достоверенность адреса'
        keyboard_raw = filters_table.legal.inlinaLegalKeyboard.keyboard_legal_address.copy()
        keyboard_raw.append(
            [InlineKeyboardButton("⬅ Назад ⬅", callback_data="LegalMenu")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard_raw)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.ADDR_LEGAL_FILTER
    elif query.data == 'prolongAddr':
        test_answer_begin = 'Адрес пролонгируется?'
        keyboard_raw = filters_table.legal.inlinaLegalKeyboard.keyboard_legal_address_prolong.copy()
        keyboard_raw.append(
            [InlineKeyboardButton("⬅ Назад ⬅", callback_data="LegalMenu")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard_raw)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.ADDR_PROLONG_FILTER
    elif query.data == 'cpoMenu':
        test_answer_begin = 'Тип CPO'
        keyboard_raw = filters_table.legal.inlinaLegalKeyboard.keyboard_legal_cpo_access.copy()
        keyboard_raw.append(
            [InlineKeyboardButton("⬅ Назад ⬅", callback_data="LegalMenu")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard_raw)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.CPO_LEGAL_FILTER
    elif query.data == 'licenseMenu':
        test_answer_begin = 'Тип лицензии'
        keyboard_raw = filters_table.legal.inlinaLegalKeyboard.keyboard_legal_license.copy()
        keyboard_raw.append(
            [InlineKeyboardButton("⬅ Назад ⬅", callback_data="LegalMenu")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard_raw)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.LICENSE_LEGAL_FILTER
    elif query.data == 'checkDir':
        test_answer_begin = 'Директор достоверен?'
        keyboard_raw = filters_table.legal.inlinaLegalKeyboard.keyboard_legal_director.copy()
        keyboard_raw.append(
            [InlineKeyboardButton("⬅ Назад ⬅", callback_data="LegalMenu")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard_raw)
        cr_user.filter_stage = tgUser.TgInnUserFilterStage.DIR_LEGAL_FILTER
    await query.edit_message_text(text=test_answer_begin)
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def process_get_company_req(query: CallbackQuery, cr_user: tgUser.TgInnUser):
    cr_user.company_list = build_data_from_google_sheet(cr_user.query_to_table)
    if len(cr_user.company_list) != 0:
        # TODO: new logic for flow filters
        for filters in cr_user.filter_methods_lst:
            cr_user.company_list = filters.filter_method(cr_user.company_list, filters.arg)

    test_answer_begin = "Доброго дня! Данный бот помогает выгрузить компании из доступных в вашей базе данных!\n" \
                        "Выберите регион, настройте фильтры или сделайте прямой запрос по ИНН!"

    if len(cr_user.query_to_table.region) != 0:
        region_lst = []
        for region in cr_user.query_to_table.region:
            region_lst.append(inlineKeyBoardCollections.keyboard_regions_dict[region])
        region_str = ";".join(region_lst)
        test_answer_begin = test_answer_begin + '\n' + f'Ваши регионы работы: ' + region_str

    test_answer_begin = build_filter_msg_info(cr_user, test_answer_begin)
    test_answer_begin = f"По вашим фильтрам выгружено: {len(cr_user.company_list)} компаний"

    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_base_company_get)
    await query.edit_message_text(text=test_answer_begin)
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def process_get_batch_of_company(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                       cr_user: tgUser.TgInnUser):
    msg_batch_company = await cr_user.build_msg_from_batch_of_company(cr_user.get_batch_of_company())
    for msg in msg_batch_company:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        await asyncio.sleep(1)

    reply_markup = InlineKeyboardMarkup(inlineKeyBoardCollections.keyboard_base_company_get)
    text_answer = 'Пачка компаний отправлена выше несколькими сообщениями. Вы можете продолжить выгружать компании или ' \
                  'сбросить фильтры для нового запроса.'

    if len(cr_user.query_to_table.region) != 0:
        region_lst = []
        for region in cr_user.query_to_table.region:
            region_lst.append(inlineKeyBoardCollections.keyboard_regions_dict[region])
        region_str = ";".join(region_lst)
        text_answer = text_answer + '\n' + f'Ваши регионы работы: ' + region_str

    text_answer = build_filter_msg_info(cr_user, text_answer)
    text_answer = text_answer + f"\nПо вашим фильтрам выгружено: {len(cr_user.company_list)} компаний"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_answer, reply_markup=reply_markup)


def build_filter_msg_info(current_user: tgUser.TgInnUser, msg: str) -> str:
    if len(current_user.filter_methods_lst) == 0:
        return msg
    msg = msg + '\n\n' + "Ваши фильтры для получения компаний. \n"
    for filter_method in current_user.filter_methods_lst:
        msg = msg + filter_method.filter_method_readable + ": " + filter_method.arg_readable + '\n'
    return msg
 