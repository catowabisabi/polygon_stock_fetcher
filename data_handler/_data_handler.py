import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_handler.short_squeeze_scanner2 import ShortSqueezeScanner
from utils._polygon.polygon_premarket_fetcher import PolygonController
from polygon import RESTClient
from polygon.rest.models import TickerSnapshot

from get_sec_filings.get_sec_filings_6_demo_cache import SECFinancialAnalyzer
from utils._database._mongodb.mongo_handler import MongoHandler

from zoneinfo import ZoneInfo
from utils.logger.shared_logger import logger
from datetime import datetime, timedelta
import time
import json

from openai import OpenAI
from api_polygon.api_chart import ChartAnalyzer
from utils._news.api_news_fetcher import RVLNewsAnalyzer



from utils.newsfilter_api import NewsfilterAPI


class SymbolMerger:
    def __init__(self, all_keys):
        self.all_keys = all_keys
        self.ny_today = datetime.now(ZoneInfo("America/New_York")).strftime('%Y-%m-%d')
        self.ny_tz = ZoneInfo("America/New_York")
        
    def merge(self, list_of_symbols, fundamentals, price_results):
        # Create mappings from symbols to their respective data
        symbol_map_fundamentals = {item['symbol']: item for item in fundamentals if item.get('symbol')}
        symbol_map_prices = {item['symbol']: item for item in price_results if item.get('symbol')}

        merged_results = []
        for symbol in list_of_symbols:
            record = {key: None for key in self.all_keys}
            record['symbol'] = symbol

            if symbol in symbol_map_fundamentals:
                record.update(symbol_map_fundamentals[symbol])
            if symbol in symbol_map_prices:
                record.update(symbol_map_prices[symbol])

            merged_results.append(record)

        return merged_results


class DataHandler:
    """
    調試版本的 DataHandler - 添加詳細日誌以找出保存問題
    """
    
    def __init__(self):
        self.polygon_controller = PolygonController()
        self.mongo_handler = MongoHandler()
        self.mongo_handler.create_collection('fundamentals_of_top_list_symbols')
        self.squeeze_scanner = ShortSqueezeScanner()
        
        # 數據存儲屬性
        self.fundamentals = []
        self.list_of_symbols = []
        self._db_cache = {}
        self.ny_today = datetime.now(ZoneInfo("America/New_York")).strftime('%Y-%m-%d')
        self.ny_tz = ZoneInfo("America/New_York")

    def _get_db_documents(self, symbols=None, force_refresh=False):
        """統一的數據庫文檔獲取方法，帶緩存機制"""
        if symbols is None:
            symbols = self.list_of_symbols
            
        cache_key = f"{'-'.join(sorted(symbols))}_{self.ny_today}"
        
        if not force_refresh and cache_key in self._db_cache:
            logger.info(f"Using cached data for {len(symbols)} symbols")
            return self._db_cache[cache_key]
        
        logger.info(f"Querying database for {len(symbols)} symbols on {self.ny_today}")
        documents = self.mongo_handler.find_doc(
            "fundamentals_of_top_list_symbols",
            {
                "symbol": {"$in": symbols},
                "today_date": self.ny_today
            }
        )
        
        logger.info(f"Found {len(documents)} documents in database")
        self._db_cache[cache_key] = documents
        return documents

    def check_merge_errors(self):
        """檢查合併錯誤"""
        error_data = self.mongo_handler.find_doc(
            "fundamentals_of_top_list_symbols",
            {"close_change_percentage": {"$exists": False}}
        )
        print(f"Length of error data: {len(error_data)}")
        if len(error_data) > 0:
            logger.warning(f"Error: 已找到 {len(error_data)} 個錯誤: Symbols: {error_data[0]['symbol']}")
            logger.warning(f"Error in fundamental data for symbol: {error_data[0]['symbol']}")
            
            # 刪除錯誤數據
            for error_doc in error_data:
                try:
                    self.mongo_handler.delete_doc(
                        "fundamentals_of_top_list_symbols",
                        {"close_change_percentage": {"$exists": False}}
                    )
                    logger.info(f"已刪除錯誤數據: {error_doc['symbol']}")
                except Exception as e:
                    logger.error(f"刪除錯誤數據時出錯 {error_doc['symbol']}: {e}")
                    exit()
            
            logger.info(f"已刪除所有錯誤數據")
        else:
            logger.info(f"No errors in fundamental data")
        return False

    def get_fundamentals(self, symbol):
        """Get fundamental data for a single symbol using Polygon API."""
        try:
            details = self.polygon_controller.polygon_client.get_ticker_details(ticker=symbol)
            if not details or not hasattr(details, 'results'):
                return {'symbol': symbol}
            
            results = details.results
            return {
                'symbol': symbol,
                'name': results.get('name'),
                'listingExchange': results.get('primary_exchange'),
                'securityType': 'Common Stock' if results.get('type') == 'CS' else results.get('type'),
                'sector': results.get('sic_description'),
                'industry': results.get('sic_description'),
                'market': results.get('market'),
                'outstandingShares': {'$numberLong': str(results.get('share_class_shares_outstanding', 0))},
                'countryDomicile': 'US' if results.get('locale') == 'us' else results.get('locale'),
                'isin': None,
                'float': {'$numberLong': str(results.get('weighted_shares_outstanding', 0))},
                'annualDividend': None,
                'dividendFrequency': None,
                'beta': None,
                'bookValue': None,
                'earningsPerShare': None,
                'earningsPerShareTTM': None,
                'forwardEarningsPerShare': None,
                'turnoverPercentage': None,
                'averageVolume3M': None,
                'optionable': True,
                'lotSize': results.get('round_lot'),
                'lastSplitInfo': None,
                'lastSplitDate': None,
                'polygon_details': {
                    'active': results.get('active'),
                    'address': {
                        'address1': results.get('address', {}).get('address1'),
                        'city': results.get('address', {}).get('city'),
                        'postal_code': results.get('address', {}).get('postal_code'),
                        'state': results.get('address', {}).get('state')
                    },
                    'branding': {
                        'icon_url': results.get('branding', {}).get('icon_url'),
                        'logo_url': results.get('branding', {}).get('logo_url')
                    },
                    'cik': results.get('cik'),
                    'composite_figi': results.get('composite_figi'),
                    'currency_name': results.get('currency_name'),
                    'description': results.get('description'),
                    'homepage_url': results.get('homepage_url'),
                    'list_date': results.get('list_date'),
                    'market_cap': results.get('market_cap'),
                    'phone_number': results.get('phone_number'),
                    'share_class_figi': results.get('share_class_figi'),
                    'sic_code': results.get('sic_code'),
                    'ticker_root': results.get('ticker_root'),
                    'total_employees': results.get('total_employees'),
                    'weighted_shares_outstanding': results.get('weighted_shares_outstanding')
                },
                'today_date': datetime.now(ZoneInfo("America/New_York")).strftime('%Y-%m-%d')
            }
        except Exception as e:
            logger.error(f"Error fetching fundamentals for {symbol}: {e}")
            return {'symbol': symbol}

    def get_list_of_fundamentals(self, list_of_symbols):
        """Get fundamental data for multiple symbols using Polygon API."""
        fundamentals = []
        for symbol in list_of_symbols:
            fundamental = self.get_fundamentals(symbol)
            fundamentals.append(fundamental)
        return fundamentals

    def get_analyzer_data(self, symbol):
        """Get market data for a single symbol using ChartAnalyzer."""
        try:
            # 使用新的 ChartAnalyzer 來獲取和分析數據
            analyzer = ChartAnalyzer(symbol)
            result = analyzer.run()
            
            # 將分析結果轉換為所需的格式
            return {
                'symbol': symbol,
                'premarket_high': result['premarket_high'],
                'premarket_low': result['premarket_low'],
                'market_open_high': result['market_open_high'],
                'market_open_low': result['market_open_low'],
                'day_high': result['day_high'],
                'day_low': result['day_low'],
                'day_close': result['day_close'],
                'yesterday_close': result['yesterday_close'],
                'high_change_percentage': result['high_change_percentage'],
                'close_change_percentage': result['close_change_percentage'],
                'most_volume_high': result['most_volume_high'],
                'most_volume_low': result['most_volume_low'],
                'key_levels': result.get('key_levels', []),
                '1m_chart_data': result['1m_chart_data'],
                '5m_chart_data': result['5m_chart_data'],
                '1d_chart_data': result['1d_chart_data']
            }
            
        except Exception as e:
            logger.error(f"Error in get_analyzer_data for {symbol}: {e}")
            return {
                'symbol': symbol,
                'premarket_high': None,
                'premarket_low': None,
                'market_open_high': None,
                'market_open_low': None,
                'day_high': None,
                'day_low': None,
                'day_close': None,
                'yesterday_close': None,
                'high_change_percentage': None,
                'close_change_percentage': None,
                'most_volume_high': None,
                'most_volume_low': None,
                'key_levels': [],
                '1m_chart_data': [],
                '5m_chart_data': [],
                '1d_chart_data': []
            }

    def fmt(self, value):
        """Format numeric values."""
        return round(value, 2) if isinstance(value, (int, float)) else value

    def get_price_analyzer_results(self, list_of_symbols):
        """Get price analysis results for multiple symbols."""
        price_analyzer_results = []
        for symbol in list_of_symbols:
            result = self.get_analyzer_data(symbol)
            price_analyzer_results.append(result)
            #print(result['1m_chart_data'][-1]['datetime'])
            #   print(result['5m_chart_data'][-1]['datetime'])
            #print(result['1d_chart_data'][-1]['datetime'])
        return price_analyzer_results

    def merge_fundamentals_and_price_data(self, list_of_symbols, fundamentals, price_analyzer_results):
        """Merge fundamental data with price analysis data."""
        # Define all possible fields
        all_keys = [
            'symbol', 'name', 'listingExchange', 'securityType', 'countryDomicile', 'countryIncorporation',
            'isin', 'sector', 'industry', 'lastSplitInfo', 'lastSplitDate', 'lotSize', 'optionable',
            'earningsPerShare', 'earningsPerShareTTM', 'forwardEarningsPerShare', 'nextEarnings',
            'annualDividend', 'last12MonthDividend', 'lastDividend', 'exDividend', 'dividendFrequency',
            'beta', 'averageVolume3M', 'turnoverPercentage', 'bookValue', 'sales', 'outstandingShares', 'float',
            # Add price fields
            'premarket_high', 'premarket_low', 'market_open_high', 'market_open_low', 'day_high', 'day_low',
            'day_close', 'yesterday_close', 'high_change_percentage', 'close_change_percentage',
            'most_volume_high', 'most_volume_low'
        ]

        merger = SymbolMerger(all_keys)
        return merger.merge(list_of_symbols, fundamentals, price_analyzer_results)

    def perform_short_squeeze_analysis(self):
        """Perform short squeeze analysis on fundamental data."""
        logger.info("Starting Short Squeeze Analysis")
        list_of_short_squeeze_results = []
        
        for fundamental in self.fundamentals:
            short_squeeze_results = self.squeeze_scanner.run(
                new_stock_data=fundamental,
                current_price=fundamental['day_close'],
                intraday_high=fundamental['day_high'],
                short_interest=None,
                as_json=True
            )
            list_of_short_squeeze_results.append(short_squeeze_results)
            logger.info(f"Short Squeeze Analysis for {fundamental['symbol']} Ready!")
            #self.squeeze_scanner.print_readable_analysis()

        logger.info(f"Short Squeeze Analysis Lengths: {len(list_of_short_squeeze_results)}")
        
        # 優化的合併方法：直接字典更新
        squeeze_results_map = {item['symbol']: item for item in list_of_short_squeeze_results if item.get('symbol')}
        
        for fundamental_item in self.fundamentals:
            symbol = fundamental_item.get('symbol')
            if symbol and symbol in squeeze_results_map:
                # 直接更新現有的 fundamental 字典，避免覆蓋重要字段
                squeeze_data = squeeze_results_map[symbol].copy()
                squeeze_data.pop('symbol', None)  # 移除 symbol 鍵避免重複
                fundamental_item.update(squeeze_data)
                logger.info(f"Short Squeeze Analysis Merged into Fundamentals for {symbol} !")
        
        logger.info(f"Successfully merged short squeeze analysis for {len(squeeze_results_map)} symbols")
        return self.fundamentals

    def handle_symbols(self, list_of_symbols):
        """Process symbols to get fundamentals, price data, and short squeeze analysis."""
        logger.info(f"處理 {len(list_of_symbols)} 個符號的數據")
        
        # Get price analysis results
        price_analyzer_results = self.get_price_analyzer_results(list_of_symbols)
        logger.info(f"獲取到 {len(price_analyzer_results)} 個價格分析結果")
        
        # Get fundamental data
        fundamentals = self.get_list_of_fundamentals(list_of_symbols)
        logger.info(f"獲取到 {len(fundamentals)} 個基本面數據")
        
        # Merge fundamental and price data
        self.fundamentals = self.merge_fundamentals_and_price_data(list_of_symbols, fundamentals, price_analyzer_results)
        logger.info(f"合併後的基本面數據長度: {len(self.fundamentals)}")
        
        # 檢查合併後數據的結構
        if self.fundamentals:
            sample_keys = list(self.fundamentals[0].keys())
            logger.info(f"樣本數據字段: {sample_keys[:10]}...")  # 只顯示前10個字段
        
        # Perform short squeeze analysis
        return self.perform_short_squeeze_analysis() #return fundamentals with short squeeze analysis

    def store_fundamentals_in_db(self):
        """Store or update fundamental data in MongoDB - 添加詳細調試信息"""
        logger.info(f"開始保存 {len(self.fundamentals)} 個基本面數據到數據庫")
        
        # 檢查數據完整性
        for i, fundamental in enumerate(self.fundamentals):
            if not fundamental.get('symbol'):
                logger.error(f"第 {i} 個基本面數據缺少 symbol 字段: {fundamental}")
                continue
            
            # 檢查是否有必要的價格數據
            required_fields = ['day_close', 'close_change_percentage']
            missing_fields = [field for field in required_fields if field not in fundamental or fundamental[field] is None]
            if missing_fields:
                logger.warning(f"Symbol {fundamental['symbol']} 缺少字段: {missing_fields}")
        
        ny_time = datetime.now(ZoneInfo("America/New_York"))
        ny_today = ny_time.strftime('%Y-%m-%d')
        date_list = [(ny_time - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        
        logger.info(f"查詢最近 7 天的數據: {date_list}")

        # Query recent fundamental documents
        recent_fundamental_docs = self.mongo_handler.find_doc(
            "fundamentals_of_top_list_symbols",
            {
                "symbol": {"$in": [f["symbol"] for f in self.fundamentals]},
                "today_date": {"$in": date_list}
            }
        )
        
        logger.info(f"找到 {len(recent_fundamental_docs)} 個最近的基本面文檔")
        recent_symbols = set(doc["symbol"] for doc in recent_fundamental_docs)
        
        # 保存計數器
        saved_count = 0
        updated_count = 0

        for fundamental in self.fundamentals:
            symbol = fundamental["symbol"]
            fundamental["today_date"] = ny_today

            # 取出這個 symbol 最近 7 天的舊資料
            recent_docs = [doc for doc in recent_fundamental_docs if doc["symbol"] == symbol]
            
            if recent_docs:
                # 找到最新的那筆（若有多筆）
                latest_doc = max(recent_docs, key=lambda d: d["today_date"])

                # 保留舊資料中其他字段，更新為新資料（新資料優先）
                merged_data = {**latest_doc, **fundamental}
                merged_data["today_date"] = ny_today  # 一定是今天

                try:
                    result = self.mongo_handler.upsert_doc(
                        "fundamentals_of_top_list_symbols",
                        {"symbol": symbol, "today_date": ny_today},
                        merged_data
                    )
                    logger.info(f"更新 {symbol}：合併舊資料後保存為今天的資料")
                    updated_count += 1
                except Exception as e:
                    logger.error(f"更新 {symbol} 時出錯: {e}")
            else:
                # 沒有舊資料，直接插入今天的資料
                try:
                    result = self.mongo_handler.upsert_doc(
                        "fundamentals_of_top_list_symbols",
                        {"symbol": symbol, "today_date": ny_today},
                        fundamental
                    )
                    logger.info(f"新增 {symbol} 為今天的新資料")
                    saved_count += 1
                except Exception as e:
                    logger.error(f"儲存 {symbol} 時出錯: {e}")

        
        # 驗證保存結果
        time.sleep(1)
        verification_docs = self.mongo_handler.find_doc(
            "fundamentals_of_top_list_symbols",
            {
                "symbol": {"$in": [f["symbol"] for f in self.fundamentals]},
                "today_date": ny_today
            }
        )
        logger.info(f"驗證: 數據庫中找到 {len(verification_docs)} 個今日文檔")
        
        # 檢查是否所有數據都已保存
        saved_symbols = set(doc["symbol"] for doc in verification_docs)
        missing_symbols = set(f["symbol"] for f in self.fundamentals) - saved_symbols
        if missing_symbols:
            logger.error(f"以下符號的數據未能保存到數據庫: {missing_symbols}")
        else:
            logger.info("所有基本面數據已成功保存到數據庫")

    def process_suggestions(self):
        """統一處理建議的方法 - 使用 Polygon API 的新聞數據和 OpenAI 分析"""
        logger.info("Processing suggestions...")
        
        # 獲取數據庫中已有建議的文檔
        documents = self._get_db_documents()
        existing_suggestions_symbols = {
            doc["symbol"] for doc in documents 
            if doc.get("suggestion")
        }
        
        logger.info(f"找到 {len(existing_suggestions_symbols)} 個已有建議的符號")
        
        # 找出需要分析的新符號
        symbols_to_analyze = [
            symbol for symbol in self.list_of_symbols 
            if symbol not in existing_suggestions_symbols
        ]
        
        # 為新符號獲取新聞和分析
        if symbols_to_analyze:
            logger.info(f"正在為 {len(symbols_to_analyze)} 個新符號分析建議")
            new_suggestions = []
            
            # 初始化 Summarizer (包含 OpenAI 客戶端)
            summarizer = Summarizer()
            
            for symbol in symbols_to_analyze:
                print("================================================")
                print(f"\n\n\n📰 Fetching news...:{symbol}")
                
                news_data = []  # Initialize news_data list here
                
                try:
                    # 使用 Polygon API 獲取新聞
                    news_generator = self.polygon_controller.polygon_client.list_ticker_news(
                        ticker=symbol,
                        limit=5,
                        order='desc',
                        sort='published_utc'
                    )
                    
                    # 將生成器轉換為列表
                    news_list = list(news_generator) if news_generator else []
                    
                    if news_list:
                        # 處理新聞數據
                        for item in news_list:
                            try:
                                # 轉換時間戳為UTC時間
                                published_time = datetime.fromisoformat(item.published_utc.replace('Z', '+00:00'))
                                # 確保時間是UTC時區
                                if published_time.tzinfo is None:
                                    published_time = published_time.replace(tzinfo=ZoneInfo("UTC"))
                                utc_timestamp = int(published_time.timestamp())
                                
                                news_item = {
                                    "title": item.title,
                                    "link": item.article_url,
                                    "publisher": item.publisher.name if hasattr(item.publisher, 'name') else item.publisher,
                                    "symbols": [symbol.upper()],  # 保持與原格式一致
                                    "utcTime": utc_timestamp,
                                    "keywords": item.tickers if hasattr(item, 'tickers') else []
                                }
                                news_data.append(news_item)
                            except Exception as e:
                                logger.error(f"處理新聞項目時出錯: {e}")
                                continue

                        
                    # region Newsfilter API
                    news_filter_api = NewsfilterAPI()
                    news_filter_api_result = news_filter_api.get_news_from_newsfilter(symbol)
                    if news_filter_api_result and news_filter_api_result.get('articles'):
                        for article in news_filter_api_result['articles']:
                            try:
                                # Convert publishedAt string to UTC timestamp
                                published_time = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                                if published_time.tzinfo is None:
                                    published_time = published_time.replace(tzinfo=ZoneInfo("UTC"))
                                utc_timestamp = int(published_time.timestamp())
                                
                                news_item = {
                                    "title": article['title'],
                                    "link": article['url'],
                                    "publisher": article['source']['name'],
                                    "symbols": [symbol.upper()],
                                    "utcTime": utc_timestamp,
                                    "keywords": [],
                                    "html_content": article.get('html_content', '')  # Use get() with default value
                                }
                                print(f"🔍 ===========News Item: {news_item}")
                                news_data.append(news_item)
                            except Exception as e:
                                logger.error(f"處理 Newsfilter 新聞項目時出錯: {e}")
                                continue

                    if news_data:
                        # 使用原有的 RVLNewsAnalyzer 來處理新聞
                        news_analyzer = RVLNewsAnalyzer()
                        summaries = news_analyzer.analyze(news_data)
                        print(f"\n\n 📰 Summaries for {symbol.upper()}: {json.dumps(summaries, indent=2, ensure_ascii=False)}")
                        
                        if summaries != []:
                            suggestion = summarizer.suggestion(summaries)
                            print(f"\n\n 📰 Suggestion for {symbol.upper()}: {suggestion}")
                        else:
                            suggestion = "No recent news available"
                        
                        new_suggestions.append({"symbol": symbol, "suggestion": suggestion})
                        
                        # 保存到數據庫
                        try:
                            result = self.mongo_handler.upsert_doc(
                                "fundamentals_of_top_list_symbols",
                                {"symbol": symbol, "today_date": datetime.now(ZoneInfo("UTC")).strftime('%Y-%m-%d')},
                                {"suggestion": suggestion}
                            )
                            logger.info(f"保存建議 {symbol}: {result}")
                        except Exception as e:
                            logger.error(f"保存建議 {symbol} 時出錯: {e}")
                    
                    else:
                        logger.warning(f"沒有找到 {symbol} 的新聞")
                        new_suggestions.append({"symbol": symbol, "suggestion": "No recent news available"})
                        
                except Exception as e:
                    logger.error(f"❌ Failed to fetch news for {symbol.upper()}: {e}")
                    if hasattr(e, "response") and e.response:
                        logger.error(f"Status Code: {e.response.status_code}")
                        logger.error(f"Response: {e.response.text}")
                    new_suggestions.append({"symbol": symbol, "suggestion": f"Error fetching news: {str(e)}"})

            # 刷新緩存
            self._get_db_documents(force_refresh=True)
            
            # 打印新建議
            self.print_readable_suggestions(new_suggestions)
            
            return len(new_suggestions)
        
        logger.info("No new symbols need suggestion analysis")
        return 0

    def process_sec_analysis(self):
        """統一處理SEC分析的方法"""
        logger.info("Processing SEC filing analysis...")
        
        # 獲取已有SEC分析的符號
        documents = self._get_db_documents()
        analyzed_symbols = {
            doc["symbol"] for doc in documents 
            if doc.get("sec_filing_analysis")
        }
        
        logger.info(f"找到 {len(analyzed_symbols)} 個已有SEC分析的符號")
        
        # 找出需要分析的符號
        symbols_to_analyze = [
            symbol for symbol in self.list_of_symbols 
            if symbol not in analyzed_symbols
        ]
        
        if symbols_to_analyze:
            logger.info(f"正在為 {len(symbols_to_analyze)} 個符號分析SEC文件")
            analyzer = SECFinancialAnalyzer()
            analyzer.SYMBOL_LIST = symbols_to_analyze
            analysis_results = analyzer.run_analysis()

            # 直接更新到數據庫
            for analysis_result in analysis_results:
                symbol = analysis_result["Symbol"]
                try:
                    result = self.mongo_handler.upsert_doc(
                        "fundamentals_of_top_list_symbols",
                        {"symbol": symbol, "today_date": self.ny_today},
                        {"sec_filing_analysis": analysis_result}
                    )
                    logger.info(f"保存SEC分析 {symbol}: {result}")
                except Exception as e:
                    logger.error(f"保存SEC分析 {symbol} 時出錯: {e}")
            
            # 刷新緩存
            self._get_db_documents(force_refresh=True)
            
            return len(analysis_results)
        
        logger.info("No new symbols need SEC analysis")
        return 0

    def build_final_results(self):
        """構建最終結果"""
        logger.info("Building final results...")
        
        # 獲取所有今日的基本面文檔
        documents = self._get_db_documents()
        
        # 構建最終結果
        final_fundamentals = []
        final_sec_analyses = []
        
        for doc in documents:
            # 基本面數據
            final_fundamentals.append(doc)
            
            # SEC分析結果（如果存在）
            if "sec_filing_analysis" in doc:
                final_sec_analyses.append(doc["sec_filing_analysis"])
        
        logger.info(f"Final results: {len(final_fundamentals)} fundamentals, {len(final_sec_analyses)} SEC analyses")
        
        return final_fundamentals, final_sec_analyses

    def print_readable_suggestions(self, suggestions: list[dict]):
        """Print suggestions in a human-readable format."""
        for item in suggestions:
            symbol = item.get("symbol", "Unknown symbol")
            suggestion = item.get("suggestion", "(No suggestion content)")

            print("====================================")
            print(f"📌 Suggestion for {symbol}:\n\n")
            print(suggestion)
            print("\n")

    def get_positions(self):
        """Placeholder for retrieving current positions from trading account."""
        pass

    def get_accounts(self):
        """Placeholder for retrieving account information."""
        pass

    def run(self, list_of_symbols):
        """
        調試版本的主執行方法
        """
        logger.info(f"=== 開始運行 DataHandler，處理 {len(list_of_symbols)} 個符號 ===")
        logger.info(f"符號列表: {list_of_symbols}")
        
        self.list_of_symbols = list_of_symbols
        self._db_cache.clear()  # 清空緩存
        
        # Step 1: 處理符號並獲取基本面數據和分析
        logger.info("=== Step 1: 處理符號和基本面數據 ===")
        self.fundamentals = self.handle_symbols(self.list_of_symbols) #return fundamentals with short squeeze analysis
        
        if not self.fundamentals:
            logger.error("❌ 沒有獲取到任何基本面數據！")
            return [], []
        
        logger.info(f"✅ 成功處理 {len(self.fundamentals)} 個基本面數據")
        
        # Step 2: 將基本面數據存儲到數據庫
        logger.info("=== Step 2: 存儲基本面數據到數據庫 ===")
        self.store_fundamentals_in_db()
        
        # Step 3: 處理建議
        logger.info("=== Step 3: 處理建議 ===")
        new_suggestions_count = self.process_suggestions()
        
        # Step 4: 處理SEC分析
        logger.info("=== Step 4: 處理SEC分析 ===")
        new_analyses_count = self.process_sec_analysis()
        
        # Step 5: 構建最終結果
        logger.info("=== Step 5: 構建最終結果 ===")
        final_fundamentals, final_sec_analyses = self.build_final_results()
        
        # Step 6: 檢查合併錯誤
        logger.info("=== Step 6: 檢查合併錯誤 ===")
        self.check_merge_errors()
        
        logger.info(f"""
        === 處理完成！ ===
        - 處理符號數量: {len(self.list_of_symbols)}
        - 新建議數量: {new_suggestions_count}
        - 新SEC分析數量: {new_analyses_count}
        - 返回基本面數據: {len(final_fundamentals)}
        - 返回SEC分析: {len(final_sec_analyses)}
        """)
        
        return final_fundamentals, final_sec_analyses

class Summarizer:
    def __init__(self):
        self.key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.key)

    def summarize(self, text: str) -> str:
        prompt = f"請根據以下新聞內容生成繁體中文簡短摘要：\n\n{str(text)}"
        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant. You take news content as input and generate a detailed summary. Do not include the original news content in the summary."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = completion.choices[0].message.content.strip()
        print(f"\n📰 Summary: {summary}\n")
        return summary

    def suggestion(self, text: str) -> str:
        prompt = f"請根據以下新聞內容生成簡短建議：\n\n{str(text)}"
        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "developer", "content": "用戶是一個日內交易者, 他主要的是做空股票的交易者, 用戶會提供最新的新聞的一些總結, 如果新聞中有非常強的正面情緒, 請向用戶列出風險, 解釋為何不建議做空, 但如果沒有當天的新聞, 或新聞中的正面情緒不高, 請向用戶列出建議。"},
                {"role": "user", "content": prompt}
            ]
        )
        summary = completion.choices[0].message.content.strip()
        print(f"\n📰 Summary: {summary}\n")
        return summary