import logging
import os
from datetime import datetime

# 設置日誌配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 創建共用的 logger
logger = logging.getLogger("PolygonStockFetcher")

# 確保 logs 目錄存在
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# 設置文件處理器
file_handler = logging.FileHandler(
    os.path.join(logs_dir, f'polygon_fetcher_{datetime.now().strftime("%Y%m%d")}.log'),
    encoding='utf-8'
)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)