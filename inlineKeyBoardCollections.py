from telegram import InlineKeyboardButton

keyboard_base = [
    [InlineKeyboardButton("🗺️ Выбрать регион работы 🗺️", callback_data="RegChoice")],
    [InlineKeyboardButton("✉ Прямой поиск по ИНН ✉", callback_data="InnRequest")],
    [InlineKeyboardButton("📁 Юр.фильтры 📁", callback_data="LegalMenu"),
     InlineKeyboardButton("🗞️ Формат сделки 🗞️", callback_data="DealMenu"),
     ],
    [InlineKeyboardButton("💹 Обороты/Налог режим 💹", callback_data="CashFlow")],
    [InlineKeyboardButton("🔨 Осн. ОКВЭД 🔨", callback_data="BaseOkv"),
     InlineKeyboardButton("⚙ Доп. ОКВЭД ⚙", callback_data="AddOkv")],
    [InlineKeyboardButton("⏳ Дата регистрации ⏳", callback_data="DateReg")],
    [InlineKeyboardButton("💳 Налоговый орган 💳", callback_data="TaxController")],
    [InlineKeyboardButton("🗃 Участие в гос.контрактах 🗃", callback_data="GovermentChoicer")],
    [InlineKeyboardButton("🏯 Выбор типа компании 🏯", callback_data="CompanyType")],
    [InlineKeyboardButton("💼 Мои фильтры 💼", callback_data="MyFilters")]
]

keyboard_base_filters_on = [
    [InlineKeyboardButton("🗺️ Выбрать регион работы 🗺️", callback_data="RegChoice")],
    [InlineKeyboardButton("✉ Прямой поиск по ИНН ✉", callback_data="InnRequest")],
    [InlineKeyboardButton("📁 Юр.фильтры 📁", callback_data="LegalMenu"),
     InlineKeyboardButton("🗞️ Формат сделки 🗞️", callback_data="DealMenu"),
     ],
    [InlineKeyboardButton("💹 Обороты/Налог режим  💹", callback_data="CashFlow")],
    [InlineKeyboardButton("🔨 Осн. ОКВЭД 🔨", callback_data="BaseOkv"),
     InlineKeyboardButton("⚙ Доп. ОКВЭД ⚙", callback_data="AddOkv")],
    [InlineKeyboardButton("⏳ Дата регистрации ⏳", callback_data="DateReg")],
    [InlineKeyboardButton("💳 Налоговый орган 💳", callback_data="TaxController")],
    [InlineKeyboardButton("🗃 Участие в гос.контрактах 🗃", callback_data="GovermentChoicer")],
    [InlineKeyboardButton("🏯 Выбор типа компании 🏯", callback_data="CompanyType")],
    [InlineKeyboardButton("💼 Мои фильтры 💼", callback_data="MyFilters")],
    [InlineKeyboardButton("🧾 Сохранить текущие фильтры 🧾", callback_data="SaveFilters")],
    [InlineKeyboardButton("❌ Убрать фильтрацию ❌", callback_data="EraseFilters")],
    [InlineKeyboardButton("⏬ Получить компании ⏬", callback_data="GetComp")]
]

keyboard_base_company_get = [
    [InlineKeyboardButton("🗺️ Выбрать регион работы 🗺️", callback_data="RegChoice")],
    [InlineKeyboardButton("✉ Прямой поиск по ИНН ✉", callback_data="InnRequest")],
    [InlineKeyboardButton("📁 Юр.фильтры 📁", callback_data="LegalMenu"),
     InlineKeyboardButton("🗞️ Формат сделки 🗞️", callback_data="DealMenu"),
     ],
    [InlineKeyboardButton("💹 Обороты/Налог режим  💹", callback_data="CashFlow")],
    [InlineKeyboardButton("🔨 Осн. ОКВЭД 🔨", callback_data="BaseOkv"),
     InlineKeyboardButton("⚙ Доп. ОКВЭД ⚙", callback_data="AddOkv")],
    [InlineKeyboardButton("⏳ Дата регистрации ⏳", callback_data="DateReg")],
    [InlineKeyboardButton("💳 Налоговый орган 💳", callback_data="TaxController")],
    [InlineKeyboardButton("🗃 Участие в гос.контрактах 🗃", callback_data="GovermentChoicer")],
    [InlineKeyboardButton("🏯 Выбор типа компании 🏯", callback_data="CompanyType")],
    [InlineKeyboardButton("💼 Мои фильтры 💼", callback_data="MyFilters")],
    [InlineKeyboardButton("🧾 Сохранить текущие фильтры 🧾", callback_data="SaveFilters")],
    [InlineKeyboardButton("❌ Убрать фильтрацию ❌", callback_data="EraseFilters")],
    [InlineKeyboardButton("⏬ Получить 5 компаний ⏬", callback_data="GetCompFive")]
]

keyboard_regions = [
    [InlineKeyboardButton("⭐ Москва и МО ⭐", callback_data="MscReg")],
    [InlineKeyboardButton("🏛️ СПБ и ЛО 🏛", callback_data="SpbReg")],
    [InlineKeyboardButton("🌇 Регионы 🌇", callback_data="FarReg")],
    [InlineKeyboardButton("⬅ Назад ⬅", callback_data="BackToMain")]
]

keyboard_legal_filters = [
    [InlineKeyboardButton("🏭 Достовер. адрес 🏭", callback_data="checkAddr")],
    [InlineKeyboardButton("⏩ Пролонгация адреса ⏩", callback_data="prolongAddr")],
    [InlineKeyboardButton("🕴️ Достовер. директора 🕴️", callback_data="checkDir")],
    [InlineKeyboardButton("👛 CPO 👛", callback_data="cpoMenu")],
    [InlineKeyboardButton("📜 Лицензии 📜", callback_data="licenseMenu")],
    [InlineKeyboardButton("⬅ Назад ⬅", callback_data="BackToMain")]
]

keyboard_cashflow_filters = [
    [InlineKeyboardButton("💴 Обороты за 2021 💴", callback_data="flow2021")],
    [InlineKeyboardButton("💶 Обороты за 2022 💶", callback_data="flow2022")],
    [InlineKeyboardButton("💴 Обороты за 2023 💴", callback_data="flow2023")],
    [InlineKeyboardButton("💶 Обороты за 2024 💶", callback_data="flow2024")],
    [InlineKeyboardButton("📜 Налоговый режим 📜", callback_data="TaxMode")],
    [InlineKeyboardButton("⬅ Назад ⬅", callback_data="BackToMain")]
]

keyboard_back_to_menu = [
    [InlineKeyboardButton("⬅ Назад ⬅", callback_data="BackToMain")]
]

keyboard_load_delete_filters = [
    [InlineKeyboardButton("📜 Загрузить фильтр 📜", callback_data="LoadFilters")],
    [InlineKeyboardButton("❌ Удалить фильтр ❌", callback_data="DeleteFilters")],
    
]

keyboard_deal_filters = [
    [InlineKeyboardButton("🔀 Смена 🔀", callback_data="DealChange")],
    [InlineKeyboardButton("🏃 Дир. на ЗП 🏃‍", callback_data="DirSalaryChange")],
    [InlineKeyboardButton("⬅ Назад ⬅", callback_data="BackToMain")]
]

keyboard_company_in_gov_filters = [
    [InlineKeyboardButton("🧧 Есть гос.контракты 🧧", callback_data="CompanyInGov")],
    [InlineKeyboardButton("🔒 Нет гос.контрактов 🔒", callback_data="CompanyNotInGov")],
    [InlineKeyboardButton("⬅ Назад ⬅", callback_data="BackToMain")]
]

keyboard_regions_dict = {
    "MscReg": "Мск и МО",
    "SpbReg": "Спб и ЛО",
    "FarReg": "Регионы"
}

keyboard_save_filter_navi = [
    [InlineKeyboardButton("🔜 След.10 сохр 🔜", callback_data="NextBatchFilters")],
    [InlineKeyboardButton("🔙 Предю.10 сохр 🔙", callback_data="PreviusBatchFilters")]
]

keyboard_back_to_menu_from_filter = [
    [InlineKeyboardButton("⬅ Назад в меню ⬅", callback_data="BackToMain")]
]

keyboard_find_filter_by_name = [
    [InlineKeyboardButton("🔎 Поиск сохр. фильтра по названию 🔍", callback_data="FindSaveFilterByName")]
]


#######################
keyboard_deal_type_dict = {
    "Change": "Смена",
    "MoneyDir": "на ЗП"
}

keyboard_list_of_comp_processing = [
    [InlineKeyboardButton("Выгрузить еще 5 компаний 📝", callback_data="LoadComp5")],
    [InlineKeyboardButton("Новый запрос ✍", callback_data="NewReq")],
]
