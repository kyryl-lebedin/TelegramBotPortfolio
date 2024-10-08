import datetime

import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
import inlineKeyBoardCollections
import pandas as pd

from tgUser import FilterQuery

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "speed_id"


def get_table(region_str):
    range_name = f"'{inlineKeyBoardCollections.keyboard_regions_dict[region_str]}'!A:AD"
    try:
        creds_robot = ServiceAccountCredentials.from_json_keyfile_name('cred/key.json',
                                                                   scopes=SCOPES).authorize(httplib2.Http())
        service = build("sheets", "v4", http=creds_robot)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        return values

    except HttpError as err:
        print(err)


def build_data_from_google_sheet(filter_to_table: FilterQuery) -> pd.DataFrame:
    list_of_vals = []
    for i, regions in enumerate(filter_to_table.region):
        if i != 0:
            list_of_vals = list_of_vals + get_table(regions)[1:]
        else:
            list_of_vals = list_of_vals + get_table(regions)
    table_df = pd.DataFrame(list_of_vals)
    if len(table_df) == 0:
        return table_df
    table_df.rename(columns=table_df.iloc[0], inplace=True)
    table_df = table_df.iloc[1:]
    table_df['Оборот за 2021'] = table_df['Оборот за 2021'].replace('', 'Без оборотов')
    table_df['Оборот за 2022'] = table_df['Оборот за 2022'].replace('', 'Без оборотов')
    table_df['Оборот за 2023'] = table_df['Оборот за 2023'].replace('', 'Без оборотов')
    table_df['Оборот за 2024'] = table_df['Оборот за 2024'].replace('', 'Без оборотов')
    return table_df


def get_company_by_direct_inn_request(filter_to_table: FilterQuery, target_inn) -> pd.DataFrame:
    table_df = build_data_from_google_sheet(filter_to_table)
    filter_str = table_df['ИНН'].str.contains(str(target_inn), na=False, case=False)
    table_df = table_df[filter_str].reset_index(drop=True)
    return table_df
