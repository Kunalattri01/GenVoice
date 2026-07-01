import requests

API_KEY = "6c8b7431-3a3b-4b49-98ae-59a0501386f9"

def get_top_news():
    url = "https://eventregistry.org/api/v1/article/getArticles"

    payload = {
        "apiKey": API_KEY,
        "action": "getArticles",
        "keyword": "news",
        "articlesCount": 20,
        "articlesSortBy": "date"
    }

    response = requests.get(url, params=payload)

    if response.status_code == 200:
        return response.json()

    return {}