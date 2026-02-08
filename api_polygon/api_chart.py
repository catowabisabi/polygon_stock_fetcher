import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bson import json_util
import time
from datetime import datetime, time as dtime, timedelta
from zoneinfo import ZoneInfo
from polygon import RESTClient
import logging

logger = logging.getLogger(__name__)

class ChartAnalyzer:
    def __init__(self, symbol: str, data_delay_minutes: int = 15):
        self.symbol = symbol
        self.polygon_api_key = os.getenv("POLYGON_KEY")
        if not self.polygon_api_key:
            raise ValueError("Polygon API key not found")
            
        self.client = RESTClient(self.polygon_api_key)
        self.market_open_time = dtime(9, 30)
        self.ny_tz = ZoneInfo("America/New_York")
        self.data_delay_minutes = data_delay_minutes  # 數據延遲（分鐘）

        print(f"🔍 正在為 {self.symbol} 獲取圖表數據...")
        # 初始化時獲取數據
        self.data_1m = self.get_1m()
        self.update_last_day_data()
        self.data_5m = self.get_5m()
        self.data_1d = self.get_1d()
        print(f"✅ {self.symbol} 圖表數據準備就緒")

    def __repr__(self):
        return f"<ChartAnalyzer(symbol={self.symbol})>"

    def update_last_day_data(self):
        """從 self.data_1m 中提取最後一個交易日的資料"""
        if not self.data_1m:
            self.last_day_data_1m = []
            return

        all_dates = sorted(set(x["datetime"].date() for x in self.data_1m))
        if all_dates:
            last_date = all_dates[-1]
            self.last_day_data_1m = [x for x in self.data_1m if x["datetime"].date() == last_date]
        else:
            self.last_day_data_1m = []

    def get_adjusted_now(self):
        """獲取考慮數據延遲的調整時間"""
        ny_now = datetime.now(self.ny_tz)
        adjusted_now = ny_now - timedelta(minutes=self.data_delay_minutes)
        logger.info(f"實際時間: {ny_now.strftime('%H:%M:%S')}, 調整後時間: {adjusted_now.strftime('%H:%M:%S')} (延遲{self.data_delay_minutes}分鐘)")
        return adjusted_now
    
    def get_1m(self):
        """獲取1分鐘K線數據 - 從今天4:15 AM (ET)開始，考慮數據延遲"""
        # 获取调整后的时间
        adjusted_now = self.get_adjusted_now()
        
        # 计算纽约时间的今天4:15 AM
        ny_today_415am = adjusted_now.replace(hour=4, minute=15, second=0, microsecond=0)
        
        # 如果调整后时间早于今天4:15 AM，则使用昨天的4:15 AM
        if adjusted_now < ny_today_415am:
            ny_today_415am = ny_today_415am - timedelta(days=1)
        
        # 确保不会请求未来的数据
        if adjusted_now <= ny_today_415am:
            logger.warning(f"調整後時間 {adjusted_now} 早於開始時間 {ny_today_415am}，返回空數據")
            return []
        
        # 转换为 UTC 时间并获取毫秒时间戳
        today_415am_utc = ny_today_415am.astimezone(self.ny_tz)
        adjusted_now_utc = adjusted_now.astimezone(self.ny_tz)
        
        from_timestamp = int(today_415am_utc.timestamp() * 1000)
        to_timestamp = int(adjusted_now_utc.timestamp() * 1000)
        
        try:
            aggs = []
            for a in self.client.list_aggs(
                ticker=self.symbol,
                multiplier=1,
                timespan='minute',
                from_=from_timestamp,  # 使用毫秒时间戳
                to=to_timestamp,       # 使用毫秒时间戳
                adjusted=True,
                sort="asc",
                limit=1000
            ):
                aggs.append(a)
            
            return [
                {
                    "datetime": datetime.fromtimestamp(a.timestamp/1000, self.ny_tz),
                    "open": a.open,
                    "high": a.high,
                    "low": a.low,
                    "close": a.close,
                    "volume": a.volume
                }
                for a in aggs
            ] if aggs else []
            
        except Exception as e:
            error_msg = str(e)
            if "NOT_AUTHORIZED" in error_msg:
                logger.warning(f"1m數據需要升級Polygon.io計劃: {error_msg}")
            else:
                logger.error(f"Error fetching 1m data: {e}")
            return []

    def get_5m(self):
        """獲取5分鐘K線數據 - 從前天4:15 AM (ET)開始，考慮數據延遲"""
        adjusted_now = self.get_adjusted_now()
        ny_two_days_ago = adjusted_now - timedelta(days=2)
        ny_two_days_ago_415am = ny_two_days_ago.replace(hour=4, minute=15, second=0, microsecond=0)

        logger.info(f"5m數據開始時間: {ny_two_days_ago_415am}")
        
        if adjusted_now.time() < dtime(4, 15):
            ny_two_days_ago_415am = ny_two_days_ago_415am - timedelta(days=1)
        
        two_days_ago_415am_utc = ny_two_days_ago_415am.astimezone(ZoneInfo("UTC"))
        adjusted_now_utc = adjusted_now.astimezone(ZoneInfo("UTC"))
        
        from_timestamp = int(two_days_ago_415am_utc.timestamp() * 1000)
        to_timestamp = int(adjusted_now_utc.timestamp() * 1000)

        #print(from_timestamp)
        #print(to_timestamp)

        
        try:
            aggs = []
            for a in self.client.list_aggs(
                ticker=self.symbol,
                multiplier=5,
                timespan='minute',
                from_=from_timestamp,
                to=to_timestamp,
                adjusted=True,
                sort="asc",
                limit=1000
            ):
                aggs.append(a)
            
            if not aggs:
                logger.warning(f"No 5m data returned for {self.symbol}")
                return []
            
            data = [
                {
                    "datetime": datetime.fromtimestamp(a.timestamp/1000, self.ny_tz),
                    "open": a.open,
                    "high": a.high,
                    "low": a.low,
                    "close": a.close,
                    "volume": a.volume
                }
                for a in aggs
            ]
            
            logger.info(f"Retrieved {len(data)} 5m candles for {self.symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching 5m data for {self.symbol}: {e}")
            return []

    def get_1d(self):
        """獲取日K線數據 - 過去兩年，考慮數據延遲"""
        # 獲取調整後的紐約時間
        adjusted_now = self.get_adjusted_now()
        
        # 计算纽约时间两年前的日期
        ny_two_years_ago = adjusted_now - timedelta(days=730)
        
        # 如果调整后时间早于4:15 AM，则使用前一天作为结束日期
        if adjusted_now.time() < dtime(4, 15):
            adjusted_now = adjusted_now - timedelta(days=1)
        
        # 转换为 UTC 时间
        two_years_ago_utc = ny_two_years_ago.astimezone(ZoneInfo("UTC"))
        adjusted_now_utc = adjusted_now.astimezone(ZoneInfo("UTC"))
        
        try:
            aggs = self.client.get_aggs(
                ticker=self.symbol,
                multiplier=1,
                timespan='day',
                from_=two_years_ago_utc.strftime('%Y-%m-%d'),
                to=adjusted_now_utc.strftime('%Y-%m-%d'),
                limit=500
            )
            
            return [
                {
                    "datetime": datetime.fromtimestamp(a.timestamp/1000, self.ny_tz),
                    "open": a.open,
                    "high": a.high,
                    "low": a.low,
                    "close": a.close,
                    "volume": a.volume
                }
                for a in aggs
            ] if aggs else []
            
        except Exception as e:
            logger.error(f"Error fetching daily data: {e}")
            return []

    # 保持原有的分析方法不變
    def to_two_decimal(self, value):
        return round(value, 2) if value is not None else None

    def get_premarket_data(self):
        return [x for x in self.last_day_data_1m if x["datetime"].time() < self.market_open_time]

    def get_market_data(self):
        return [x for x in self.last_day_data_1m if x["datetime"].time() >= self.market_open_time]

    def get_premarket_high(self):
        premarket = self.get_premarket_data()
        return self.to_two_decimal(max(x["high"] for x in premarket)) if premarket else None

    def get_premarket_low(self):
        premarket = self.get_premarket_data()
        return self.to_two_decimal(min(x["low"] for x in premarket)) if premarket else None

    def get_market_open_high(self, time_range=("09:31", "09:45")):
        try:
            start = dtime(*map(int, time_range[0].split(":")))
            end = dtime(*map(int, time_range[1].split(":")))

            if not self.data_1m:
                return None

            last_date = self.data_1m[-1]["datetime"].date()
            opens = [
                x for x in self.data_1m
                if x["datetime"].date() == last_date and start <= x["datetime"].time() <= end
            ]

            highs = [x["high"] for x in opens if "high" in x]
            return self.to_two_decimal(max(highs)) if highs else None

        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing time range: {time_range}, error: {e}")
            return None

    def get_market_open_low(self, time_range=("09:31", "09:45")):
        try:
            start = dtime(*map(int, time_range[0].split(":")))
            end = dtime(*map(int, time_range[1].split(":")))

            if not self.data_1m:
                return None

            last_date = self.data_1m[-1]["datetime"].date()
            opens = [
                x for x in self.data_1m
                if x["datetime"].date() == last_date and start <= x["datetime"].time() <= end
            ]

            lows = [x["low"] for x in opens if "low" in x]
            return self.to_two_decimal(min(lows)) if lows else None

        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing time range: {time_range}, error: {e}")
            return None

    def get_day_high(self):
        if not self.last_day_data_1m:
            return None
        return self.to_two_decimal(max(x["high"] for x in self.last_day_data_1m))

    def get_day_low(self):
        market_data = self.get_market_data()
        if not market_data:
            return None
        return self.to_two_decimal(min(x["low"] for x in market_data))

    def get_day_close(self):
        if not self.last_day_data_1m:
            return None
        sorted_data = sorted(self.last_day_data_1m, key=lambda x: x["datetime"])
        return self.to_two_decimal(sorted_data[-1]["close"])

    def get_yesterday_close(self):
        if len(self.data_1d) < 2:
            return None
        sorted_data = sorted(self.data_1d, key=lambda x: x["datetime"])
        return self.to_two_decimal(sorted_data[-2]["close"])

    def get_high_change_percentage(self):
        y_close = self.get_yesterday_close()
        d_high = self.get_day_high()
        if y_close and d_high:
            return round((d_high - y_close) / y_close * 100, 2)
        return None

    def get_close_change_percentage(self):
        y_close = self.get_yesterday_close()
        d_close = self.get_day_close()
        if y_close and d_close:
            return round((d_close - y_close) / y_close * 100, 2)
        return None

    def get_most_volume_high(self):
        greens = [x for x in self.last_day_data_1m if x["close"] >= x["open"] and x["volume"] > 0]
        if not greens:
            return None
        most = max(greens, key=lambda x: x["volume"])
        return self.to_two_decimal(most["high"])

    def get_most_volume_low(self):
        market_data = self.get_market_data()
        reds = [x for x in market_data if x["close"] < x["open"] and x["volume"] > 0]
        if not reds:
            return None
        most = max(reds, key=lambda x: x["volume"])
        return self.to_two_decimal(most["low"])

    def _get_volume_since_4am(self):
        four_am = dtime(4, 0)
        market_data = [x for x in self.data_5m if x["datetime"].time() >= four_am]
        return sum(x["volume"] for x in market_data) if market_data else 0

    def get_key_levels(self, level_number=5):
        current_volume = self._get_volume_since_4am()
        day_high = self.get_day_high()
        if day_high is None:
            return []

        daily_candles = self.data_1d
        if not daily_candles:
            return []

        filtered_candles = [
            candle for candle in daily_candles 
            if candle["volume"] > current_volume and candle["high"] > day_high
        ]

        if not filtered_candles:
            return []

        key_levels = []
        for candle in filtered_candles:
            if candle["low"] > day_high:
                key_levels.append(self.to_two_decimal(candle["low"]))
            else:
                key_levels.append(self.to_two_decimal(candle["high"]))

        key_levels = sorted(list(set(key_levels)))
        return key_levels[:level_number]

    def run(self):
        """執行分析並返回所有數據點"""
        result = {
            "symbol": self.symbol,
            "premarket_high": self.get_premarket_high(),
            "premarket_low": self.get_premarket_low(),
            "market_open_high": self.get_market_open_high(),
            "market_open_low": self.get_market_open_low(),
            "day_high": self.get_day_high(),
            "day_low": self.get_day_low(),
            "day_close": self.get_day_close(),
            "yesterday_close": self.get_yesterday_close(),
            "high_change_percentage": self.get_high_change_percentage(),
            "close_change_percentage": self.get_close_change_percentage(),
            "most_volume_high": self.get_most_volume_high(),
            "most_volume_low": self.get_most_volume_low(),
            "key_levels": self.get_key_levels(),
            "1m_chart_data": self.data_1m,
            "5m_chart_data": self.data_5m,
            "1d_chart_data": self.data_1d
        }
        return result

if __name__ == "__main__":
    #symbol = input("請輸入股票代號（如 TSLA）: ").strip().upper()
    symbol = "TSLA"
    # 測試延遲數據配置（默認15分鐘延遲）
    analyzer = ChartAnalyzer(symbol, data_delay_minutes=15)
    result = analyzer.run()
    print(f"數據延遲配置: {analyzer.data_delay_minutes} 分鐘")
    print(f"1m數據數量: {len(result['1m_chart_data'])}")
    if result['1m_chart_data']:
        print(f"1m數據時間範圍: {result['1m_chart_data'][0]['datetime']} 到 {result['1m_chart_data'][-1]['datetime']}")
    print(f"5m數據數量: {len(result['5m_chart_data'])}")
    if result['5m_chart_data']:
        print(f"5m數據時間範圍: {result['5m_chart_data'][0]['datetime']} 到 {result['5m_chart_data'][-1]['datetime']}")
    print(f"1d數據數量: {len(result['1d_chart_data'])}")
    if result['1d_chart_data']:
        print(f"最新日K線: {result['1d_chart_data'][-1]}")
    #print(json_util.dumps(result, indent=2, ensure_ascii=False))