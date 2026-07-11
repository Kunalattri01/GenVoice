import requests

API_KEY = "413ad0d5-089a-48cb-85fa-2297d50769d5" # Live

# API_KEY = "a8dd4f60-189d-4dbe-ae24-138106893eaa" # Development

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