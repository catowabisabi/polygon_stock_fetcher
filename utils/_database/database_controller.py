from _mongodb.mongo_handler import MongoHandler

from utils.logger.logger import logger
from datetime import datetime
import pytz


class DatabaseController:
    def __init__(self):
        self.mongo_handler = MongoHandler()

    def initialize_database_collections(self, today_top_list_doc_name = "today_top_list", fundamentals_of_top_list_symbols_doc_name = "fundamentals_of_top_list_symbols"):
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Setting up Collections for {today_top_list_doc_name} and {fundamentals_of_top_list_symbols_doc_name}")
        self.mongo_handler.create_collection(today_top_list_doc_name)
        self.mongo_handler.create_collection(fundamentals_of_top_list_symbols_doc_name)







