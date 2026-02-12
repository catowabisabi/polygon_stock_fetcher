import requests

class NewsfilterAPI:
    @staticmethod
    def get_news_from_newsfilter(symbols: str):
        url = f"https://news.enomars.org/news/symbol/{symbols}"

        try:
            response = requests.get(url, timeout=180)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "no news found"}
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    news = NewsfilterAPI.get_news_from_newsfilter("aapl")
    print(f"新聞: {news}")

    # API returns a list directly, or a dict with 'error' key
    if isinstance(news, list) and len(news) > 0:
        print(f"Found {len(news)} news articles")
        for article in news:
            print(f"  - {article.get('title')} ({article.get('source')})")
    elif isinstance(news, dict) and 'error' in news:
        print("Error occurred:", news['error'])
    else:
        print("No news found or unexpected response format")