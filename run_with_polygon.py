import pytz
from datetime import datetime, timedelta
from utils.logger.logger import logger 
from data_handler._data_handler import DataHandler
from utils._telegram.telegram_notifier import TelegramNotifier
from utils._polygon.polygon_premarket_fetcher import PolygonController
from utils._database.database_controller import DatabaseController
from dotenv import load_dotenv
load_dotenv(override=True)

    
#region MAIN
def main(debug = False):
    try:
        dbc = DatabaseController()
        dbc.initialize_database_collections()

        #region Get Top Gainers
        pc = PolygonController()
        top_gainers_price_data = pc.get_top_gainers_data(debug=debug)
        top_gainers_symbols = pc.get_top_gainers_list()
        filtered_top_gainers_symbols = pc.get_filtered_top_gainers_list()
        clean_filtered_top_gainers_symbols = pc.clean_symbols(filtered_top_gainers_symbols) #['SBET', 'MBAVW', 'FAAS']
        #endregion

       #region DataHandler
        data_handler = DataHandler()

        
        top_gainners_fundamentals, sec_analysis_results = data_handler.run(clean_filtered_top_gainers_symbols) #top_gainners_symbols contain all data of every top gainers
  

        print(top_gainners_fundamentals[0]['1m_chart_data'][0])
        print("\n\n\n\n")
    except Exception as e:
        error_msg = f"程序執行出錯：{str(e)}\n請檢查日誌獲取詳細信息。"
        send_msg_to_telegram(error_msg)
        logger.error(f"Error in main: {str(e)}")
        raise


    #

#region Wrapped Main in a Scheduler,
# this scheduler is to check if it should run in a specific time period.
from utils._scheduler.trade_scheduler import TradingScheduler
def scheduled_main():
    scheduler = TradingScheduler()
    if scheduler.should_run_now(debug=False):
        try:
            main()
            print(f"✅ Execution completed at {datetime.now(pytz.timezone('US/Eastern'))}")
        except Exception as e:
            print(f"❌ Error during execution: {e}")
    else:
        print(f"⏳ Skipped at {datetime.now(pytz.timezone('US/Eastern'))} (Outside trading time or not the interval)")



# region Scheduler (run every minute)
import schedule
import time
def schedule_jobs(callback):
    logger.info("\n\nScheduler started. Press Ctrl+C to exit.")
    schedule.every(1).minutes.do(callback)
    while True:
        schedule.run_pending()
        time.sleep(1)

def send_msg_to_telegram(msg):
    try:
        notifier = TelegramNotifier()
        return notifier.send_message(msg)
    except Exception as e:
        print(f"發送 Telegram 消息時發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    main()
    schedule_jobs(lambda: scheduled_main())
    
    

    