legal_choice_filter_query = ['checkAddr', 'prolongAddr', 'cpoMenu', 'licenseMenu', 'checkDir']

addr_legal_address_lst = ['addr_ok', 'addr_warning']
dir_legal_lst = ['dir_ok', 'dir_warning']
legal_address_prolong_lst = ['addr_cont_ok', 'addr_cont_not']
legal_cpo_access_lst = ['not_cpo', 'cpo_before', 'cpo_constr_90', 'cpo_constr_500', 'cpo_constr_3mld', 'cpo_develop_25', 'cpo_develop_50', 'cpo_research']
legal_license_lst = ['not_license', 'alko_license', 'atom_license', 'home_license', 'lombard_license', 'med_license',
                     'metall_license', 'cul_license', 'it_license', 'mfo_license', 'alert_license', 'edu_license', 'logic_license',
                     'rostech_license', 'tbo_license', 'comm_license', 'farma_license', 'far_loc_license', 'fsb_secret', 'fsb_license',
                     'sec_license', 'sec_ar_license', 'other_license']

addr_legal_address_dict = {'addr_ok': 'Достоверенный', 'addr_warning': 'Недостоверенный'}
dir_legal_dict = {'dir_ok': 'Достоверенный', 'dir_warning': 'Недостоверенный'}
legal_address_prolong_dict = {'addr_cont_ok': 'С пролонгацией', 'addr_cont_not': 'Без пролонгации'}
legal_cpo_access_dict = {'not_cpo': 'Без СРО', 'cpo_before': 'Допуск СРО был ранее', 'cpo_constr_90': 'Строительное СРО до 90 млн',
                        'cpo_constr_500': 'Строительное СРО до 500 млн', 'cpo_constr_3mld': 'Строительное СРО до 3 млрд',
                        'cpo_develop_25': 'Проектное СРО до 25 млн', 'cpo_develop_50': 'Проектное СРО до 50 млн',
                        'cpo_research': 'СРО изыскания'}
legal_license_dict = {'not_license': 'Без лицензий', 'alko_license': 'Алкогольная лицензия', 'atom_license': 'Атомная лицензия',
                      'home_license': 'ЖКХ лицензия', 'lombard_license': 'Ломбард лицензия', 'med_license': 'Медицинская лицензия',
                      'metall_license': 'Металлы лицензия', 'cul_license': 'Минкульт лицензия', 'it_license': 'Минцифры (IT компании)',
                      'mfo_license': 'МФО', 'alert_license': 'МЧС лицензия', 'edu_license': 'Образовательная лицензия',
                      'logic_license': 'Перевозки лицензия', 'rostech_license': 'РосТехНадзор', 'tbo_license': 'Лицензия ТБО',
                      'comm_license': 'Связь лицензия', 'farma_license': 'Фармацевтическая лицензия опт',
                      'far_loc_license': 'Фармацевтическая лицензия розница', 'fsb_secret': 'ФСБ тайна','fsb_license': 'ФСБ шифр лицензия',
                      'sec_license': 'ЧОП лицензия', 'sec_ar_license': 'ЧОП лицензия с оружием', 'other_license': 'Другая лицензия'}
