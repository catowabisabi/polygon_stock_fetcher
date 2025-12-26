# 🤖 Polygon Stock Fetcher - 股票數據獲取工具

> 基於 Polygon.io API 的全方位股票數據獲取與分析工具

---

## 📋 目錄
- [專案簡介](#專案簡介)
- [快速開始](#快速開始)
- [主要功能](#主要功能)
- [環境設置](#環境設置)
- [主要文件說明](#主要文件說明)
- [使用方法](#使用方法)
- [一鍵啟動](#一鍵啟動)
- [數據流程圖](#數據流程圖)
- [常見問題](#常見問題)

---

## 🚀 快速開始

### TL;DR - 立即啟動

```bash
# 方法 1: 雙擊批次文件（最簡單）
雙擊 start_polygon_fetcher.bat 或 quick_start.bat

# 方法 2: 命令列啟動
.\start_polygon_fetcher.bat

# 方法 3: 手動啟動（如果環境已設置）
C:\Users\admin\anaconda3\envs\Polygon_stock_fetcher\python.exe run_with_polygon.py
```

### 環境資訊

- **Conda 環境名稱**: `Polygon_stock_fetcher`
- **Python 版本**: 3.13.2
- **環境路徑**: `C:\Users\admin\anaconda3\envs\Polygon_stock_fetcher`
- **主程式**: `run_with_polygon.py`

### 必要的 API Keys

創建 `.env` 文件在專案根目錄：

```bash
POLYGON_KEY=your_polygon_api_key_here
MONGODB_CONNECTION_STRING=your_mongodb_connection_string  # 可選
TELEGRAM_BOT_TOKEN=your_bot_token                          # 可選
TELEGRAM_CHAT_ID=your_chat_id                              # 可選
```

---

## 🐳 Docker 部署 / Docker Deployment (TrueNAS SCALE)

### 必要條件 / Prerequisites
- TrueNAS SCALE 24.10 以上版本並啟用 Docker / Docker Compose 支援。
- 具有 Shell 或 Apps CLI 操作權限。
- 已在專案根目錄建立 `.env`，內容與上述環境變數相同。

### 建構與部署步驟 / Build & Run Steps
1. **複製程式碼至資料集** / Clone this repo into a dataset that TrueNAS can mount。
2. **建置映像** / Build the image：
  ```bash
  docker compose build
  ```
3. **啟動服務** / Start the service：
  ```bash
  docker compose up -d
  ```
4. TrueNAS SCALE 會自動建立 `cache/` 與 `logs/` 卷，用於保存快取與日誌。

### 容器設置重點 / Container Notes
- 基底映像為 `python:3.11-slim`，並預先安裝 Google Chrome 以支援 Headless 自動化。
- `docker-compose.yml` 已將時區設為 `America/New_York`，可依需求覆寫。
- 如果需要連線到外部 MongoDB，請在 `.env` 中設定 `MONGODB_CONNECTION_STRING`。
- Windows 專用的 ZeroPro 自動化模組不會在容器中啟用，但不影響主要資料抓取流程。

### 常用維運指令 / Operations
```bash
# 查看日誌 / Tail logs
docker compose logs -f

# 重新啟動服務 / Restart service
docker compose restart

# 停止並移除容器 / Stop and remove
docker compose down
```

---

## 專案簡介

這是一個功能完整的股票數據獲取與分析系統，整合 Polygon.io API 來獲取實時市場數據。系統能自動掃描市場中的漲幅股票，進行基本面分析、SEC文件檢索，並通過 Telegram 發送通知。

### 🚀 主要功能

- **實時數據獲取** - 使用 Polygon.io API 獲取實時市場數據
- **Top Gainers 追蹤** - 自動掃描並追蹤當日漲幅最大的股票
- **基本面分析** - 獲取股票財務數據與基本面資料
- **SEC 文件檢索** - 自動獲取與分析 SEC 申報文件
- **技術分析** - 內建技術指標與圖表分析工具
- **新聞分析** - 整合新聞數據進行情感分析
- **數據庫支援** - 支援 MongoDB 與 SQLite 數據存儲
- **定時調度** - 自動化執行，只在交易時間運行
- **Telegram 通知** - 重要資訊即時推送

---

## 🗂 主要文件說明

### 核心文件

#### 1. `run_with_polygon.py` - 主程式入口
**功能**：
- 程式主入口，協調所有模組運作
- 獲取 Top Gainers 數據並進行篩選
- 調用 DataHandler 進行數據處理與分析
- 整合定時調度器（每分鐘檢查是否該執行）
- 錯誤處理與 Telegram 通知

**使用時機**：
- 直接運行此文件即可啟動整個系統

#### 2. `environment.yml` - Conda 環境配置
**功能**：
- 定義專案所需的所有 Python 套件與依賴
- 環境名稱：`tradebot`（實際安裝為 `Polygon_stock_fetcher`）
- 包含數據分析套件（pandas, numpy, scipy）
- 包含可視化工具（matplotlib, plotly）
- 包含 API 客戶端（requests, polygon-api）

**使用方法**：
```bash
conda env create -f environment.yml
conda activate Polygon_stock_fetcher
```

---

### 主要模組目錄

#### 3. `api_polygon/` - Polygon API 整合
**主要文件**：
- `polygon_controller.py` - Polygon API 控制器（較舊版本）
- `polygon_api_handler.py` - API 處理器
- `api_chart.py` - 圖表數據分析

**功能**：處理 Polygon.io API 的所有請求與響應

#### 4. `data_handler/` - 數據處理中心
**主要文件**：
- `_data_handler.py` - **核心數據處理器**
  - 協調各種數據獲取與分析
  - 整合基本面、新聞、SEC 文件等數據
  - 使用 AI 進行新聞分析
  - 數據合併與結構化
  
- `short_squeeze_scanner2.py` - Short Squeeze 掃描器
  - 檢測可能的 short squeeze 機會
  
- `merge_data.py` - 數據合併工具

**功能**：所有數據的處理、分析與整合

#### 5. `utils/` - 工具函式庫

**子目錄結構**：

- **`_polygon/polygon_premarket_fetcher.py`**
  - **PolygonController 類**：新版 Polygon API 控制器
  - 獲取 Top Gainers 列表
  - 過濾符合條件的股票（價格、成交量等）
  - 清理股票代碼

- **`_database/database_controller.py`**
  - 數據庫初始化與管理
  - 支援 MongoDB 與 SQLite
  
- **`_news/api_news_fetcher.py`**
  - 新聞數據獲取
  - 使用 RVL News API
  
- **`_telegram/telegram_notifier.py`**
  - Telegram Bot 通知功能
  - 發送交易信號與錯誤警報
  
- **`_scheduler/trade_scheduler.py`**
  - 交易時間檢查
  - 確保只在美股交易時間執行
  
- **`logger/logger.py`**
  - 日誌記錄系統
  - 統一的日誌格式

#### 6. `get_sec_filings/` - SEC 文件處理
**主要文件**：
- `get_sec_filings_6_demo_cache.py` - **SECFinancialAnalyzer 類**
  - 獲取公司的 SEC 申報文件
  - 財務數據分析
  - 使用緩存機制加速

---

## ⚙️ 環境設置

### 前置需求
- Python 3.13
- Anaconda 或 Miniconda
- Polygon.io API Key
- （可選）MongoDB 連接字串
- （可選）Telegram Bot Token

### 安裝步驟

1. **檢查 Conda 環境**
```bash
conda env list
```

2. **啟動環境**
```bash
# 使用現有環境
conda activate Polygon_stock_fetcher

# 或創建新環境
conda env create -f environment.yml
```

3. **配置環境變數**
在專案根目錄創建 `.env` 文件：
```bash
# Polygon API
POLYGON_KEY=your_polygon_api_key_here

# MongoDB (可選)
MONGODB_CONNECTION_STRING=your_mongodb_connection_string

# Telegram (可選)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# News API (可選)
NEWSFILTER_API_KEY=your_newsfilter_api_key
```

---

## 🚀 使用方法

### 基本使用

1. **啟動 Conda 環境**
```bash
conda activate Polygon_stock_fetcher
```

2. **運行主程式**
```bash
python run_with_polygon.py
```

### 程式運行流程

1. **初始化**：連接數據庫、初始化 API 客戶端
2. **獲取 Top Gainers**：從 Polygon API 獲取當日漲幅股票
3. **過濾篩選**：根據價格、成交量等條件篩選
4. **數據處理**：
   - 獲取基本面數據
   - 獲取 SEC 文件
   - 獲取新聞並分析
   - 獲取圖表數據
5. **結果輸出**：儲存到數據庫、發送 Telegram 通知
6. **定時執行**：每分鐘檢查，只在交易時間運行

### 測試模式

```bash
# 運行單次測試（不啟動調度器）
# 編輯 run_with_polygon.py 最後一行
if __name__ == "__main__":
    main(debug=True)  # 啟用 debug 模式
```

---

## ⚡ 一鍵啟動

### 方法一：使用批次文件（推薦）

專案提供了三個啟動文件：

#### 1. `start_polygon_fetcher.bat` - 完整版（推薦）
- 包含完整的環境檢查
- 顯示詳細的啟動步驟
- 錯誤提示與處理

**使用方法**：
```bash
.\start_polygon_fetcher.bat
```
或直接雙擊 `start_polygon_fetcher.bat` 文件

#### 2. `quick_start.bat` - 快速版
- 最簡化的啟動腳本
- 適合熟悉環境的用戶

**使用方法**：
```bash
.\quick_start.bat
```
或直接雙擊 `quick_start.bat` 文件

#### 3. `start_polygon_fetcher.ps1` - PowerShell 版
- 彩色輸出，介面更美觀
- 包含環境檢查與 .env 檢查

**使用方法**：
```powershell
.\start_polygon_fetcher.ps1
```

### 方法二：手動啟動

如果批次文件無法使用，可以手動啟動：

```bash
# 使用完整 Python 路徑
C:\Users\admin\anaconda3\envs\Polygon_stock_fetcher\python.exe run_with_polygon.py
```

---

## 📊 數據流程圖

```
run_with_polygon.py (主程式)
    ↓
PolygonController (獲取 Top Gainers)
    ↓
DataHandler (數據處理中心)
    ├─→ SECFinancialAnalyzer (SEC 文件)
    ├─→ ShortSqueezeScanner (Short Squeeze 分析)
    ├─→ RVLNewsAnalyzer (新聞分析)
    ├─→ ChartAnalyzer (技術分析)
    └─→ SymbolMerger (數據合併)
    ↓
DatabaseController (儲存結果)
    ↓
TelegramNotifier (發送通知)
```

---

## 🔧 常見問題

### Q: 找不到 tradebot 環境？
A: 環境實際名稱可能是 `Polygon_stock_fetcher`，使用：
```bash
conda activate Polygon_stock_fetcher
```

### Q: API Key 錯誤？
A: 確保 `.env` 文件在專案根目錄，且包含正確的 `POLYGON_KEY`

### Q: 程式沒有執行？
A: 檢查是否在交易時間內（美東時間 09:30-16:00），或使用 debug 模式測試

### Q: 如何停止程式？
A: 按 `Ctrl+C` 停止程式運行

---

## 📝 注意事項

1. **API 配額**：Polygon API 有請求限制，注意不要過度調用
2. **交易時間**：程式預設只在美股交易時間運行
3. **數據延遲**：免費版 API 可能有 15 分鐘延遲
4. **環境隔離**：使用 Conda 環境確保依賴隔離
5. **日誌檢查**：如遇問題，查看日誌文件了解詳情

---

## 📫 技術支援

如有問題，請檢查：
1. 日誌文件（logs/ 目錄）
2. API Key 是否正確配置
3. Conda 環境是否正確啟動
4. 網絡連接是否正常

---

**最後更新**：2025-12-16

#### Data Management
- **SQLite**: Lightweight local database for historical data
- **MongoDB**: Scalable cloud database for real-time data
- Automatic data backup and synchronization

### 🔧 Configuration Options

#### Data Fetching Parameters

```python
FETCH_CONFIG = {
    'timespan': '1m',           # Time interval
    'multiplier': 1,            # Time multiplier
    'limit': 50000,             # Maximum data points
    'adjusted': True,           # Adjusted for splits
    'sort': 'asc',             # Sort direction
    'cache': True              # Enable data caching
}
```

#### Database Configuration

```python
DATABASE_CONFIG = {
    'type': 'sqlite',            # 'sqlite' or 'mongodb'
    'sqlite_path': './data/stocks.db',
    'mongodb_uri': 'mongodb://localhost:27017/',
    'mongodb_db': 'stock_data'
}
```

### 📈 Sample Output

```
=== Stock Data Fetcher Results ===
Time: 2024-01-15 08:30:00 EST

AAPL Data:
- Current Price: $185.92
- Volume: 1.2M
- VWAP: $185.45
- Number of Trades: 2,500

Data Points Retrieved: 1000
Database Records Updated: 156
Cache Hit Rate: 85%
```

### 🧠 Learning Resources

- [Polygon.io API Documentation](https://polygon.io/docs)
- [Python Trading Data Analysis](https://www.quantstart.com/)
- [Technical Analysis Basics](https://www.investopedia.com/technical-analysis-4689657)

### ⚠️ Important Disclaimers

- **Not Financial Advice**: This tool is for educational and research purposes only
- **API Limits**: Respect Polygon.io API rate limits and terms of service
- **Data Accuracy**: While we strive for accuracy, always verify critical data

### 📌 Roadmap & Future Features

- [ ] **Web Interface** - Browser-based dashboard for data visualization
- [ ] **Advanced Analytics** - Machine learning-based analysis
- [ ] **Backtesting Engine** - Historical strategy testing capabilities
- [ ] **Real-time Alerts** - Price and volume movement notifications
- [ ] **Multi-Asset Support** - Support for crypto and forex data
- [ ] **Custom Indicators** - User-defined technical indicators
- [ ] **Data Export** - Multiple format export options

### 🛠 Troubleshooting

#### Common Issues

**API Connection Errors**
```bash
# Check API key configuration
python -c "import os; print(os.getenv('POLYGON_API_KEY'))"
```

**Database Connection Issues**
```bash
# Test database connectivity
python -c "from src.database import test_connection; test_connection()"
```

### 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/catowabisabi/tz_bot_lite_stock_fetcher/issues)
- **Discussions**: [GitHub Discussions](https://github.com/catowabisabi/tz_bot_lite_stock_fetcher/discussions)
- **Wiki**: [Project Wiki](https://github.com/catowabisabi/tz_bot_lite_stock_fetcher/wiki)

---

## 繁體中文

一個由 Polygon.io API 驅動的全面股票數據獲取和分析工具。本專案提供即時市場數據獲取和分析功能，包括歷史數據檢索和技術分析功能。

### 🚀 主要功能

- **即時數據** - 整合 Polygon.io API 提供即時市場數據
- **歷史數據** - 獲取和分析歷史價格數據
- **多資料庫支援** - 彈性數據存儲，支援 SQLite 和 MongoDB
- **技術分析** - 內建技術分析工具
- **自動化分析** - 進階篩選和排序演算法
- **數據視覺化** - 價格和成交量數據視覺化工具

### 🗂 專案結構

```bash
tz_bot_lite_stock_fetcher/
├── run_with_polygon.py      # 主要進入點，整合 Polygon API
├── environment.yml          # Conda 環境配置
├── api_polygon/            # Polygon API 整合模組
├── data_handler/           # 數據處理模組
├── utils/                  # 工具函數
│   ├── _database/         # 資料庫管理
│   ├── _news/             # 新聞數據處理
│   └── logger/            # 日誌工具
└── requirements.txt        # Python 依賴套件
```

### ⚙️ 安裝與設定

#### 前置要求

- Python 3.8 或更高版本
- Polygon.io API 金鑰

#### 環境設定

1. **複製儲存庫**
   ```bash
   git clone https://github.com/catowabisabi/tz_bot_lite_stock_fetcher.git
   cd tz_bot_lite_stock_fetcher
   ```

2. **建立 Conda 環境**
   ```bash
   conda env create -f environment.yml
   conda activate stockdata
   ```

3. **替代方案：pip 安裝**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置 API 金鑰**
   ```bash
   # 建立 .env 檔案並填入您的 API 憑證
   POLYGON_API_KEY=您的_polygon_api_金鑰
   ```

### 🚀 快速開始

#### 基本使用

```bash
# 執行主要數據獲取器，整合 Polygon
python run_with_polygon.py
```

#### 進階配置

```python
# 數據獲取配置範例
from api_polygon import PolygonController

controller = PolygonController(
    timespan="1m",          # 1分鐘數據
    multiplier=1,           # 時間乘數
    from_date="2024-01-01", # 開始日期
    to_date="2024-01-15"    # 結束日期
)

data = controller.get_aggs("AAPL")
```

### 📊 功能詳述

#### 數據獲取
- 即時和歷史價格數據
- 多時間框架支援（1分鐘、5分鐘、1小時、1天）
- 成交量和交易數據
- 技術指標

#### 數據管理
- **SQLite**：輕量級本地資料庫用於歷史數據
- **MongoDB**：可擴展雲端資料庫用於即時數據
- 自動數據備份和同步

### 🔧 配置選項

#### 數據獲取參數

```python
FETCH_CONFIG = {
    'timespan': '1m',           # 時間間隔
    'multiplier': 1,            # 時間乘數
    'limit': 50000,             # 最大數據點
    'adjusted': True,           # 調整分割
    'sort': 'asc',             # 排序方向
    'cache': True              # 啟用數據緩存
}
```

#### 資料庫配置

```python
DATABASE_CONFIG = {
    'type': 'sqlite',            # 'sqlite' 或 'mongodb'
    'sqlite_path': './data/stocks.db',
    'mongodb_uri': 'mongodb://localhost:27017/',
    'mongodb_db': 'stock_data'
}
```

### 📈 範例輸出

```
=== 股票數據獲取器結果 ===
時間: 2024-01-15 08:30:00 EST

AAPL 數據:
- 當前價格: $185.92
- 成交量: 1.2M
- VWAP: $185.45
- 交易次數: 2,500

獲取數據點: 1000
資料庫記錄更新: 156
緩存命中率: 85%
```

### 🧠 學習資源

- [Polygon.io API 文件](https://polygon.io/docs)
- [Python 交易數據分析](https://www.quantstart.com/)
- [技術分析基礎](https://www.investopedia.com/technical-analysis-4689657)

### ⚠️ 重要免責聲明

- **非投資建議**：此工具僅用於教育和研究目的
- **API 限制**：請遵守 Polygon.io API 速率限制和服務條款
- **數據準確性**：雖然我們致力於準確性，但重要數據請務必驗證

### 📌 路線圖與未來功能

- [ ] **網頁介面** - 基於瀏覽器的數據視覺化儀表板
- [ ] **進階分析** - 基於機器學習的分析
- [ ] **回測引擎** - 歷史策略測試功能
- [ ] **即時警報** - 價格和成交量變動通知
- [ ] **多資產支援** - 支援加密貨幣和外匯數據
- [ ] **自定義指標** - 用戶定義技術指標
- [ ] **數據導出** - 多格式導出選項

### 🛠 故障排除

#### 常見問題

**API 連線錯誤**
```bash
# 檢查 API 金鑰配置
python -c "import os; print(os.getenv('POLYGON_API_KEY'))"
```

**資料庫連線問題**
```bash
# 測試資料庫連線
python -c "from src.database import test_connection; test_connection()"
```

### 📜 授權條款

本專案使用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

### 🤝 貢獻方式

歡迎貢獻！請遵循以下步驟：

1. Fork 此儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

### 📞 支援與聯絡

- **問題回報**: [GitHub Issues](https://github.com/catowabisabi/tz_bot_lite_stock_fetcher/issues)
- **討論區**: [GitHub Discussions](https://github.com/catowabisabi/tz_bot_lite_stock_fetcher/discussions)
- **專案Wiki**: [Project Wiki](https://github.com/catowabisabi/tz_bot_lite_stock_fetcher/wiki)

---

[⬆️ Back to top / 回到頂部](#-tz-bot-lite---stock-data-fetcher)
