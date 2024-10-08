from telegram import Update
import json
from os.path import exists
import logging

from tgUser import TgInnUser
from postgres.postgres import DatabaseManager, DB_URL

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self):       
        try:
            self.user_collection = []
            self.db_manager = DatabaseManager(DB_URL)
            self.available_keys = self.db_manager.get_all_keys()
            self.add_users_to_collection()
            logger.info("UserManager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize UserManager: {e}")
            raise

    def save_users_filters(self, filter_name:str, current_user: TgInnUser):
        # save filter instance
        id = self.db_manager.save_user_filter_to_db(tg_id=current_user.tg_id, name_for_filter=filter_name)
        self.db_manager.save_filter_method_to_db(id=id, region_set=current_user.query_to_table.region, filter_list=current_user.filter_methods_lst)
     


    async def check_licence_from_user(self, upd: Update) -> str:
        msg_words = upd.message.text.split(' ')
        if len(msg_words) < 2:
            return "Register don't success. Please call '/register your-key'"
        if msg_words[1] in self.available_keys:
            self.user_collection.append(TgInnUser(upd.message.from_user.username, upd.message.from_user.id, msg_words[1]))
            self.db_manager.add_user(upd.message.from_user.username, upd.message.from_user.id, msg_words[1])
            return "Register success. You can use bot now!"
        else:
            return "Register don't success. Wrong licence key!s"

    def add_users_to_collection(self):
        users = self.db_manager.get_all_users()
        for user in users:
            self.user_collection.append(TgInnUser(user.username, user.tg_id, user.active_key))

    async def check_user_in_list(self, upd: Update) -> int:
        for i, usr in enumerate(self.user_collection):
            if upd.message.from_user.id == usr.tg_id:
                return i
        return -1

    async def check_user_in_list_query(self, upd: Update) -> int:
        for i, usr in enumerate(self.user_collection):
            if upd.callback_query.from_user.id == usr.tg_id:
                return i
        return -1
