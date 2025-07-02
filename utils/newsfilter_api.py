import requests

class NewsfilterAPI:
    @staticmethod
    def get_news_from_newsfilter(symbols: str):
        url = f"https://news.enomars.org/api/news/{symbols}"

        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "no news found"}
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    news = NewsfilterAPI.get_news_from_newsfilter("pnp")

    # Check if we got news articles
    if news and 'articles' in news and news['articles']:
        print("Found news articles:", news)
    elif news and 'error' in news:
        print("Error occurred:", news['error'])
    else:
        print("No news found or unexpected response format")