import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytz
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from polygon import RESTClient
from polygon.rest.models import TickerSnapshot
from utils.logger.logger import logger
import re
from dotenv import load_dotenv
load_dotenv(override=True)




#region Polygon Controller
class PolygonController:
    def __init__(self):
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Initializing MainController")
        
        #region INITIALIZATION
        self.ny_time = datetime.now(ZoneInfo("America/New_York"))
        self.today_str = self.ny_time.strftime('%Y-%m-%d')
        self.polygon_api_key = os.getenv("POLYGON_KEY")
        self.polygon_client = RESTClient(self.polygon_api_key)
        self.top_gainers = []
    

        
    #region Get Top Gainers
    def get_top_gainers(self): # get top gainers raw data
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Starting to get top gainers raw data")
        self.top_gainers = self.polygon_client.get_snapshot_direction(
        "stocks",
        direction="gainers",
        )
        return self.top_gainers
    
    def print_list_of_items(self, list_of_items):
        for item in list_of_items:
            print(item)
        
    def fmt(self, value):
        return round(value, 2) if isinstance(value, (int, float)) else value

    def get_top_gainers_data(self, debug = False): # get top gainers clean data
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Starting to get top gainers clean data")
        self.top_gainers_data = []
        for item in self.get_top_gainers():
            # verify this is a TickerSnapshot
            if isinstance(item, TickerSnapshot):
                row = {
                'Ticker': item.ticker,
                'Today_Open': self.fmt(item.day.open) if item.day else None,
                'Today_High': self.fmt(item.day.high) if item.day else None,
                'Today_Low': self.fmt(item.day.low) if item.day else None,
                'Today_Close': self.fmt(item.day.close) if item.day else None,
                'Today_Volume': self.fmt(item.day.volume) if item.day else None,
                #'Today_VWAP': self.fmt(item.day.vwap) if item.day else None,

                #'Prev_Open': self.fmt(item.prev_day.open) if item.prev_day else None,
                #'Prev_High': self.fmt(item.prev_day.high) if item.prev_day else None,
                #'Prev_Low': self.fmt(item.prev_day.low) if item.prev_day else None,
                'Prev_Close': self.fmt(item.prev_day.close) if item.prev_day else None,
                #'Prev_Volume': self.fmt(item.prev_day.volume) if item.prev_day else None,
                #'Prev_VWAP': self.fmt(item.prev_day.vwap) if item.prev_day else None,

                'Min_Open': self.fmt(item.min.open) if item.min else None,
                'Min_High': self.fmt(item.min.high) if item.min else None,
                'Min_Low': self.fmt(item.min.low) if item.min else None,
                'Min_Close': self.fmt(item.min.close) if item.min else None,
                'Min_Volume': self.fmt(item.min.volume) if item.min else None,
                'Min_VWAP': self.fmt(item.min.vwap) if item.min else None,

                'Today_Change': self.fmt(item.todays_change),
                'Change_%': self.fmt(item.todays_change_percent),
                }
                self.top_gainers_data.append(row)

        #print(f"Top Gainers Data: {self.top_gainers_data}")

        df = pd.DataFrame(self.top_gainers_data)
        pd.set_option('display.max_columns', None)  # 顯示所有欄位
        #print(df.to_string(index=False))


        if debug:
            logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: 1st Top Gainers Price Data: {str(self.top_gainers_data[0])}\n")
        print()   

        return self.top_gainers_data
    
    def get_top_gainers_list(self):
        list_of_top_gainer = [item.ticker for item in self.get_top_gainers()]
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Starting to get top gainers list")
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Top gainers list: {list_of_top_gainer}")
        return list_of_top_gainer
    
    def get_filtered_top_gainers_list(self):
        top_gainers_data = self.get_top_gainers_data()
        filtered_top_gainers_list = [item['Ticker'] for item in top_gainers_data 
                                   if item['Min_Close'] is not None 
                                   and item['Min_Close'] > 1 
                                   and item['Min_Close'] < 50  
                                   and item['Change_%'] > 50 
                                   and len(item['Ticker']) <= 4]
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Filtered top gainers list: {filtered_top_gainers_list}")
        return filtered_top_gainers_list
    
    def clean_symbols(self, symbols):
        clean_symbols = [re.sub(r'[^A-Z]', '', symbol) for symbol in symbols]
        logger.info(f"{datetime.now(pytz.timezone('US/Eastern'))}: Cleaned Filtered Symbols: {str(clean_symbols)}\n")
        return clean_symbols
    

if __name__ == "__main__":
    pc = PolygonController()
    top_gainers_data = pc.get_top_gainers_data()
    list_of_top_gainer = pc.get_top_gainers_list()
    """  print(top_gainers_data)
    print(list_of_top_gainer) """