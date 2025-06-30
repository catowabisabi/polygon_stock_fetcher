# 🤖 TZ Bot Lite - Stock Data Fetcher

> **Language / 語言**: [English](#english) | [繁體中文](#繁體中文)

---

## English

A comprehensive stock data fetching and analysis tool powered by Polygon.io API. This project provides real-time market data fetching and analysis capabilities for stocks, with features for historical data retrieval and technical analysis.

### 🚀 Key Features

- **Real-time Data** - Integration with Polygon.io API for live market data
- **Historical Data** - Fetch and analyze historical price data
- **Multi-Database Support** - Flexible data storage with SQLite and MongoDB options
- **Technical Analysis** - Built-in technical analysis tools
- **Automated Analysis** - Advanced filtering and ranking algorithms
- **Data Visualization** - Tools for visualizing price and volume data

### 🗂 Project Structure

```bash
polygon_stock_fetcher/
├── run_with_polygon.py      # Main entry point with Polygon API integration
├── environment.yml          # Conda environment configuration
├── api_polygon/            # Polygon API integration modules
├── data_handler/           # Data processing modules
├── utils/                  # Utility functions
│   ├── _database/         # Database management
│   ├── _news/             # News data handling
│   └── logger/            # Logging utilities
└── requirements.txt        # Python dependencies
```

### ⚙️ Installation & Setup

#### Prerequisites

- Python 3.8 or higher
- Polygon.io API key

#### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/catowabisabi/tz_bot_lite_stock_fetcher.git
   cd tz_bot_lite_stock_fetcher
   ```

2. **Create Conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate stockdata
   ```

3. **Alternative: pip installation**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   ```bash
   # Create .env file with your API credentials
   POLYGON_API_KEY=your_polygon_api_key
   ```

### 🚀 Quick Start

#### Basic Usage

```bash
# Run the main data fetcher with Polygon integration
python run_with_polygon.py
```

#### Advanced Configuration

```python
# Example configuration for data fetching
from api_polygon import PolygonController

controller = PolygonController(
    timespan="1m",          # 1-minute data
    multiplier=1,           # Time multiplier
    from_date="2024-01-01", # Start date
    to_date="2024-01-15"    # End date
)

data = controller.get_aggs("AAPL")
```

### 📊 Features in Detail

#### Data Fetching
- Real-time and historical price data
- Multiple timeframes support (1m, 5m, 1h, 1d)
- Volume and trade data
- Technical indicators

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
