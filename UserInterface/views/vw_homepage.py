from django.views import View
from django.shortcuts import render

from articles.models import Article


class HomePageView(View):

    def get(self, request):
        published = (
            Article.objects.filter(status=Article.Status.PUBLISHED, is_active=True)
            .select_related("category", "source")
            .prefetch_related("authors", "tags")
        )

        recent = list(published.order_by("-publish_date")[:10])

        context = {
            "left_news": recent[0:2],
            "hero_main": recent[2] if len(recent) > 2 else None,
            "hero_second": recent[3] if len(recent) > 3 else None,
            "sidebar_news": recent[4:10],

            "politics_news": self._by_category(published, "Politics", 5),
            "finance_news": self._by_category(published, "Finance", 6),
            "tech_news": self._by_category(published, "Technology", 6),
            "travel_news": self._by_category(published, "Travel", 6),
            "celebrities_news": self._by_category(published, "Celebrities", 5),
            "food_news": self._by_category(published, "Food", 5),
            "makeup_news": self._by_category(published, "Make-Up", 4),
            "marketing_news": self._by_category(published, "Marketing", 6),

            "popular_posts": published.order_by("-view_count")[:5],
            "must_read": published.order_by("-view_count")[5:10],

            "news": published,
        }

        return render(request, "UserInterface/homepage.html", context)

    def _by_category(self, queryset, category_name, count):
        return list(
            queryset.filter(category__name__iexact=category_name)
            .order_by("-publish_date")[:count]
        )