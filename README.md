# 🤖 TZ Bot Lite - Pennystock Fetcher

> **Language / 語言**: [English](#english) | [繁體中文](#繁體中文)

---

## English

A comprehensive premarket penny stock scanner and automation tool designed to help users automate operations on the TradeZero platform. This project provides real-time market data fetching, analysis, and automated trading capabilities for penny stocks and low-float securities.

### 🚀 Key Features

- **Premarket Scanner** - Real-time penny stock scanning during premarket hours
- **TradeZero Integration** - Seamless automation of TradeZero platform operations
- **Multi-Database Support** - Flexible data storage with SQLite and MongoDB options
- **Real-time Data** - Integration with Polygon.io API for live market data
- **Low-Float Detection** - Specialized algorithms for identifying low-float penny stocks
- **Automated Analysis** - Advanced filtering and ranking algorithms
- **Risk Management** - Built-in position sizing and risk control features

### 🗂 Project Structure

```bash
tz_bot_lite_pennystock_fetcher/
├── run_with_polygon.py      # Main entry point with Polygon API integration
├── environment.yml          # Conda environment configuration
├── data/                    # Data storage directory
├── src/                     # Source code modules
│   ├── scanner/            # Stock scanning modules
│   ├── database/           # Database management
│   ├── api/                # API integrations
│   └── utils/              # Utility functions
├── config/                 # Configuration files
├── logs/                   # Application logs
└── requirements.txt        # Python dependencies
```

### ⚙️ Installation & Setup

#### Prerequisites

- Python 3.8 or higher
- TradeZero account (for trading features)
- Polygon.io API key (for real-time data)

#### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher.git
   cd tz_bot_lite_pennystock_fetcher
   ```

2. **Create Conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate tradebot
   ```

3. **Alternative: pip installation**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   # Create .env file with your API credentials
   POLYGON_API_KEY=your_polygon_api_key
   TRADEZERO_USERNAME=your_username
   TRADEZERO_PASSWORD=your_password
   ```

### 🚀 Quick Start

#### Basic Scanner Usage

```bash
# Run the main scanner with Polygon integration
python run_with_polygon.py
```

#### Advanced Configuration

```python
# Example configuration for penny stock scanning
from src.scanner import PennystockScanner

scanner = PennystockScanner(
    price_range=(0.01, 5.00),    # Penny stock price range
    volume_threshold=100000,      # Minimum volume
    float_threshold=50000000,     # Maximum float
    premarket_only=True          # Scan premarket only
)

results = scanner.scan()
```

### 📊 Features in Detail

#### Premarket Scanner
- Scans for penny stocks with unusual volume during premarket hours
- Filters stocks based on price, volume, and float criteria
- Real-time alerts for significant price movements

#### TradeZero Automation
- Automated order placement and management
- Position tracking and profit/loss monitoring
- Risk management with stop-loss automation

#### Data Management
- **SQLite**: Lightweight local database for historical data
- **MongoDB**: Scalable cloud database for real-time data
- Automatic data backup and synchronization

### 🔧 Configuration Options

#### Scanner Parameters

```python
SCANNER_CONFIG = {
    'price_min': 0.01,           # Minimum stock price
    'price_max': 5.00,           # Maximum stock price
    'volume_min': 50000,         # Minimum daily volume
    'float_max': 100000000,      # Maximum float
    'gap_percentage': 10,        # Minimum gap percentage
    'premarket_start': '04:00',  # Premarket scan start time
    'premarket_end': '09:30'     # Premarket scan end time
}
```

#### Database Configuration

```python
DATABASE_CONFIG = {
    'type': 'sqlite',            # 'sqlite' or 'mongodb'
    'sqlite_path': './data/stocks.db',
    'mongodb_uri': 'mongodb://localhost:27017/',
    'mongodb_db': 'pennystock_data'
}
```

### 📈 Sample Output

```
=== Premarket Penny Stock Scanner Results ===
Time: 2024-01-15 08:30:00 EST

Top Gainers:
1. ABCD - $0.85 (+45.2%) | Vol: 2.1M | Float: 25M
2. EFGH - $1.23 (+38.7%) | Vol: 1.8M | Float: 18M
3. IJKL - $0.67 (+29.1%) | Vol: 3.2M | Float: 42M

Top Volume:
1. MNOP - $2.14 | Vol: 5.8M | Change: +12.3%
2. QRST - $0.92 | Vol: 4.2M | Change: +8.7%
3. UVWX - $1.56 | Vol: 3.9M | Change: +15.2%

Alerts Generated: 12
Database Records Updated: 156
```

### 🧠 Learning Resources

- [Polygon.io API Documentation](https://polygon.io/docs)
- [TradeZero Platform Guide](https://www.tradezero.co/)
- [Penny Stock Trading Strategies](https://www.investopedia.com/articles/trading/penny-stock-trading-strategies/)
- [Python Trading Bot Development](https://www.quantstart.com/)

### ⚠️ Important Disclaimers

- **Risk Warning**: Penny stock trading involves significant risk. Past performance does not guarantee future results.
- **Not Financial Advice**: This tool is for educational and research purposes only.
- **API Limits**: Respect API rate limits and terms of service.
- **Regulatory Compliance**: Ensure compliance with local trading regulations.

### 📌 Roadmap & Future Features

- [ ] **Web Interface** - Browser-based dashboard for monitoring
- [ ] **Mobile Alerts** - Push notifications for significant events
- [ ] **Advanced Analytics** - Machine learning-based prediction models
- [ ] **Multi-Broker Support** - Integration with additional brokers
- [ ] **Backtesting Engine** - Historical strategy testing capabilities
- [ ] **Social Media Integration** - Sentiment analysis from Twitter/Reddit
- [ ] **Options Chain Analysis** - Options flow and unusual activity detection

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

**TradeZero Login Problems**
- Verify credentials in .env file
- Check for two-factor authentication requirements
- Ensure account has API access enabled

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

- **Issues**: [GitHub Issues](https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher/issues)
- **Discussions**: [GitHub Discussions](https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher/discussions)
- **Wiki**: [Project Wiki](https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher/wiki)

---

## 繁體中文

一個全面的盤前便士股掃描器和自動化工具，旨在幫助用戶自動化 TradeZero 平台的操作。本專案提供即時市場數據抓取、分析和便士股及低流通量證券的自動化交易功能。

### 🚀 主要功能

- **盤前掃描器** - 盤前時段即時便士股掃描
- **TradeZero 整合** - 無縫自動化 TradeZero 平台操作
- **多資料庫支援** - 彈性數據存儲，支援 SQLite 和 MongoDB
- **即時數據** - 整合 Polygon.io API 提供即時市場數據
- **低流通量檢測** - 專門演算法識別低流通量便士股
- **自動化分析** - 進階篩選和排序演算法
- **風險管理** - 內建倉位大小和風險控制功能

### 🗂 專案結構

```bash
tz_bot_lite_pennystock_fetcher/
├── run_with_polygon.py      # 主要進入點，整合 Polygon API
├── environment.yml          # Conda 環境配置
├── data/                    # 數據存儲目錄
├── src/                     # 原始碼模組
│   ├── scanner/            # 股票掃描模組
│   ├── database/           # 資料庫管理
│   ├── api/                # API 整合
│   └── utils/              # 工具函數
├── config/                 # 配置文件
├── logs/                   # 應用程式日誌
└── requirements.txt        # Python 依賴套件
```

### ⚙️ 安裝與設定

#### 前置要求

- Python 3.8 或更高版本
- TradeZero 帳戶（用於交易功能）
- Polygon.io API 金鑰（用於即時數據）

#### 環境設定

1. **複製儲存庫**
   ```bash
   git clone https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher.git
   cd tz_bot_lite_pennystock_fetcher
   ```

2. **建立 Conda 環境**
   ```bash
   conda env create -f environment.yml
   conda activate tradebot
   ```

3. **替代方案：pip 安裝**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置 API 金鑰**
   ```bash
   # 建立 .env 檔案並填入您的 API 憑證
   POLYGON_API_KEY=您的_polygon_api_金鑰
   TRADEZERO_USERNAME=您的_使用者名稱
   TRADEZERO_PASSWORD=您的_密碼
   ```

### 🚀 快速開始

#### 基本掃描器使用

```bash
# 執行主要掃描器，整合 Polygon
python run_with_polygon.py
```

#### 進階配置

```python
# 便士股掃描配置範例
from src.scanner import PennystockScanner

scanner = PennystockScanner(
    price_range=(0.01, 5.00),    # 便士股價格範圍
    volume_threshold=100000,      # 最小成交量
    float_threshold=50000000,     # 最大流通量
    premarket_only=True          # 僅掃描盤前
)

results = scanner.scan()
```

### 📊 功能詳述

#### 盤前掃描器
- 掃描盤前時段具有異常成交量的便士股
- 根據價格、成交量和流通量標準篩選股票
- 重大價格波動的即時警報

#### TradeZero 自動化
- 自動化訂單下單和管理
- 持倉追蹤和損益監控
- 停損自動化風險管理

#### 數據管理
- **SQLite**：輕量級本地資料庫用於歷史數據
- **MongoDB**：可擴展雲端資料庫用於即時數據
- 自動數據備份和同步

### 🔧 配置選項

#### 掃描器參數

```python
SCANNER_CONFIG = {
    'price_min': 0.01,           # 最低股價
    'price_max': 5.00,           # 最高股價
    'volume_min': 50000,         # 最小日成交量
    'float_max': 100000000,      # 最大流通量
    'gap_percentage': 10,        # 最小跳空百分比
    'premarket_start': '04:00',  # 盤前掃描開始時間
    'premarket_end': '09:30'     # 盤前掃描結束時間
}
```

#### 資料庫配置

```python
DATABASE_CONFIG = {
    'type': 'sqlite',            # 'sqlite' 或 'mongodb'
    'sqlite_path': './data/stocks.db',
    'mongodb_uri': 'mongodb://localhost:27017/',
    'mongodb_db': 'pennystock_data'
}
```

### 📈 範例輸出

```
=== 盤前便士股掃描器結果 ===
時間: 2024-01-15 08:30:00 EST

漲幅榜:
1. ABCD - $0.85 (+45.2%) | 成交量: 2.1M | 流通量: 25M
2. EFGH - $1.23 (+38.7%) | 成交量: 1.8M | 流通量: 18M
3. IJKL - $0.67 (+29.1%) | 成交量: 3.2M | 流通量: 42M

成交量排行:
1. MNOP - $2.14 | 成交量: 5.8M | 漲幅: +12.3%
2. QRST - $0.92 | 成交量: 4.2M | 漲幅: +8.7%
3. UVWX - $1.56 | 成交量: 3.9M | 漲幅: +15.2%

產生警報數: 12
資料庫記錄更新: 156
```

### 🧠 學習資源

- [Polygon.io API 文件](https://polygon.io/docs)
- [TradeZero 平台指南](https://www.tradezero.co/)
- [便士股交易策略](https://www.investopedia.com/articles/trading/penny-stock-trading-strategies/)
- [Python 交易機器人開發](https://www.quantstart.com/)

### ⚠️ 重要免責聲明

- **風險警告**：便士股交易涉及重大風險。過往表現不保證未來結果。
- **非投資建議**：此工具僅用於教育和研究目的。
- **API 限制**：請遵守 API 速率限制和服務條款。
- **法規合規**：確保遵守當地交易法規。

### 📌 路線圖與未來功能

- [ ] **網頁介面** - 基於瀏覽器的監控儀表板
- [ ] **手機警報** - 重大事件推播通知
- [ ] **進階分析** - 基於機器學習的預測模型
- [ ] **多券商支援** - 整合更多券商平台
- [ ] **回測引擎** - 歷史策略測試功能
- [ ] **社群媒體整合** - Twitter/Reddit 情緒分析
- [ ] **選擇權鏈分析** - 選擇權流量和異常活動檢測

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

**TradeZero 登入問題**
- 驗證 .env 檔案中的憑證
- 檢查雙重驗證要求
- 確保帳戶已啟用 API 存取

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

- **問題回報**: [GitHub Issues](https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher/issues)
- **討論區**: [GitHub Discussions](https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher/discussions)
- **專案Wiki**: [Project Wiki](https://github.com/catowabisabi/tz_bot_lite_pennystock_fetcher/wiki)

---

[⬆️ Back to top / 回到頂部](#-tz-bot-lite---pennystock-fetcher)
