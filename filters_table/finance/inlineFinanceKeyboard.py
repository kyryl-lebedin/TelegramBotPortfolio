from telegram import InlineKeyboardButton

taxmode_arg_dict = {
    'osno': 'ОСНО',
    'ysn1': 'УСН 1%',
    'ysn3': 'УСН 3%',
    'ysn4': 'УСН 4%',
    'ysn6': 'УСН 6%',
    'ysn7': 'УСН 7%',
    'ysn10': 'УСН 10%',
    'ysn15': 'УСН 15%',
    'aysn': 'АУСН'
}

keyword_tax_mode = [
    [InlineKeyboardButton("ОСНО", callback_data="osno")],
    [InlineKeyboardButton("УСН 1%", callback_data="ysn1")],
    [InlineKeyboardButton("УСН 3%", callback_data="ysn3")],
    [InlineKeyboardButton("УСН 4%", callback_data="ysn4")],
    [InlineKeyboardButton("УСН 6%", callback_data="ysn6")],
    [InlineKeyboardButton("УСН 7%", callback_data="ysn7")],
    [InlineKeyboardButton("УСН 10%", callback_data="ysn10")],
    [InlineKeyboardButton("УСН 15%", callback_data="ysn15")],
    [InlineKeyboardButton("АУСН", callback_data="aysn")],
]

keyboard_flow_size = [
    [InlineKeyboardButton("Без оборотов", callback_data="obor0")],
    [InlineKeyboardButton("< 1 млн. руб.", callback_data="obor1")],
    [InlineKeyboardButton("> 1 млн. руб.", callback_data="obor1_3")],
    [InlineKeyboardButton("> 3 млн. руб.", callback_data="obor3_5")],
    [InlineKeyboardButton("> 5 млн. руб.", callback_data="obor5_10")],
    [InlineKeyboardButton("> 10 млн. руб.", callback_data="obor10_20")],
    [InlineKeyboardButton("> 15 млн. руб.", callback_data="obor20_50")],
    [InlineKeyboardButton("> 20 млн. руб.", callback_data="obor50_100")],
    [InlineKeyboardButton("> 50 млн. руб.", callback_data="obor100_250")],
    [InlineKeyboardButton("> 100 млн. руб.", callback_data="obor250_500")],
    [InlineKeyboardButton("> 250 млн. руб.", callback_data="obor500_1000")],
    [InlineKeyboardButton("> 500 млн. руб.", callback_data="obormldr")],
    [InlineKeyboardButton("> 1 млрд. руб.", callback_data="obormoremldr")],
]