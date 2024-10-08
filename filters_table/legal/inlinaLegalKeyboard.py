from telegram import InlineKeyboardButton

keyboard_legal_address = [
    [InlineKeyboardButton("Достоверенный", callback_data="addr_ok")],
    [InlineKeyboardButton("Недостоверенный", callback_data="addr_warning")]
]

keyboard_legal_address_prolong = [
    [InlineKeyboardButton("С пролонгацией", callback_data="addr_cont_ok")],
    [InlineKeyboardButton("Без пролонгации", callback_data="addr_cont_not")]
]

keyboard_legal_director = [
    [InlineKeyboardButton("Достоверенный рук.", callback_data="dir_ok")],
    [InlineKeyboardButton("Недостоверенный рук.", callback_data="dir_warning")]
]

keyboard_legal_cpo_access = [
    [InlineKeyboardButton("Без СРО", callback_data="not_cpo")],
    [InlineKeyboardButton("Допуск СРО был ранее", callback_data="cpo_before")],
    [InlineKeyboardButton("Строительное СРО до 90 млн", callback_data="cpo_constr_90")],
    [InlineKeyboardButton("Строительное СРО до 500 млн", callback_data="cpo_constr_500")],
    [InlineKeyboardButton("Строительное СРО до 3 млрд", callback_data="cpo_constr_3mld")],
    [InlineKeyboardButton("Проектное СРО до 25 млн", callback_data="cpo_develop_25")],
    [InlineKeyboardButton("Проектное СРО до 50 млн", callback_data="cpo_develop_50")],
    [InlineKeyboardButton("СРО изыскания", callback_data="cpo_research")]
]

keyboard_legal_license = [
    [InlineKeyboardButton("Без лицензий", callback_data="not_license")],
    [InlineKeyboardButton("Алкогольная лицензия", callback_data="alko_license")],
    [InlineKeyboardButton("Атомная лицензия", callback_data="atom_license")],
    [InlineKeyboardButton("ЖКХ лицензия", callback_data="home_license")],
    [InlineKeyboardButton("Ломбард лицензия", callback_data="lombard_license")],
    [InlineKeyboardButton("Медицинская лицензия", callback_data="med_license")],
    [InlineKeyboardButton("Металлы лицензия", callback_data="metall_license")],
    [InlineKeyboardButton("Минкульт лицензия", callback_data="cul_license")],
    [InlineKeyboardButton("Минцифры (IT компании)", callback_data="it_license")],
    [InlineKeyboardButton("МФО", callback_data="mfo_license")],
    [InlineKeyboardButton("МЧС лицензия", callback_data="alert_license")],
    [InlineKeyboardButton("Образовательная лицензия", callback_data="edu_license")],
    [InlineKeyboardButton("Перевозки лицензия", callback_data="logic_license")],
    [InlineKeyboardButton("РосТехНадзор", callback_data="rostech_license")],
    [InlineKeyboardButton("Лицензия ТБО", callback_data="tbo_license")],
    [InlineKeyboardButton("Связь лицензия", callback_data="comm_license")],
    [InlineKeyboardButton("Фармацевтическая лицензия опт", callback_data="farma_license")],
    [InlineKeyboardButton("Фармацевтическая лицензия розница", callback_data="far_loc_license")],
    [InlineKeyboardButton("ФСБ тайна", callback_data="fsb_secret")],
    [InlineKeyboardButton("ФСБ шифр лицензия", callback_data="fsb_license")],
    [InlineKeyboardButton("ЧОП лицензия", callback_data="sec_license")],
    [InlineKeyboardButton("ЧОП лицензия с оружием", callback_data="sec_ar_license")],
    [InlineKeyboardButton("Другая лицензия", callback_data="other_license")]
]


# utils for build structure
def build_callback_list_from_keyboard(keyboard: list):
    some_lst = []
    print(keyboard)
    for btn in keyboard:
        some_lst.append(btn[0].callback_data)
    print(some_lst)


def build_callback_dict_from_keyboard(keyboard: list):
    some_dct = dict()
    for btn in keyboard:
        some_dct[btn[0].callback_data] = btn[0].text
    print(some_dct)


# build_callback_list_from_keyboard(keyboard_legal_license)
# build_callback_dict_from_keyboard(keyboard_legal_license)


