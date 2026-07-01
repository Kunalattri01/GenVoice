from django.views import View
from django.shortcuts import render
import requests


class HomePageView(View):

    def get(self, request):

        url = "https://eventregistry.org/api/v1/article/getArticles"

        payload = {
            "query": {
                "$query": {
                    "$and": [
                        {
                            "keyword": "India"
                        }
                    ]
                }
            },
            "resultType": "articles",
            "articlesCount": 60,
            "apiKey": "6c8b7431-3a3b-4b49-98ae-59a0501386f9"
        }

        news_data = []

        

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                news_data = data.get("articles", {}).get("results", [])

                print("Total Articles:", len(news_data))

        except Exception as e:
            print("ERROR:", e)

        context = {
                "left_news": news_data[:2],

                "hero_main": news_data[2] if len(news_data) > 2 else None,
                "hero_second": news_data[3] if len(news_data) > 3 else None,

                "sidebar_news": news_data[4:10],

                "politics_news": news_data[10:15],

                "popular_posts": news_data[15:20],

                "must_read": news_data[20:25],

                "finance_news": news_data[25:31],

                "tech_news": news_data[31:37],

                "travel_news": news_data[37:43],

                "celebrities_news": news_data[43:48],

                "food_news": news_data[48:53],

                "makeup_news": news_data[53:57],

                "marketing_news": news_data[57:60],

                "news": news_data,
        }

        return render(request, "UserInterface/homepage.html", context)