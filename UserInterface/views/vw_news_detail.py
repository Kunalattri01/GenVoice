import logging
from urllib.parse import unquote

from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from UserInterface.utils.news_detail import (
    fetch_article_by_uri,
    get_related_articles,
    get_latest_articles,
    get_trending_articles,
    get_prev_next_articles,
    estimate_reading_time,
)

logger = logging.getLogger(__name__)

class NewsDetailView(View):
    """
    Renders a full detail page for a single Event Registry article.

    URL:     /news/<encoded_uri>/
    Example: /news/eng-9284712/

    No database is used — the article, and every sidebar/related-articles
    list, is fetched live from Event Registry on each request.
    """
    template_name = "UserInterface/news_detail.html"

    def get(self, request, encoded_uri, *args, **kwargs):
        print("Encoded URI:", encoded_uri)

        article_uri = unquote(encoded_uri)
        print("Decoded URI:", article_uri)

        article = fetch_article_by_uri(article_uri)
        print("Article:", article)

        if not article:
            raise Http404("This article could not be found or is no longer available.")

        context = self._build_context(article, request)
        return render(request, self.template_name, context)

    def _build_context(self, article, request):
        source = article.get("source") or {}
        categories = article.get("categories") or []
        concepts = article.get("concepts") or []
        location = article.get("location") or {}
        image = article.get("image")
        media = article.get("media") or []
        sentiment = article.get("sentiment")
        body = article.get("body") or ""

        # Build a small image gallery from the main image + any media items
        gallery = []
        if image:
            gallery.append(image)
        for m in media:
            m_url = m.get("url") if isinstance(m, dict) else m
            if m_url and m_url not in gallery:
                gallery.append(m_url)

        primary_category = categories[0] if categories else None

        related_articles = get_related_articles(article, count=4)
        latest_articles = get_latest_articles(exclude_uri=article.get("uri"), count=5)
        trending_articles = get_trending_articles(exclude_uri=article.get("uri"), count=5)
        prev_article, next_article = get_prev_next_articles(article)

        popular_tags = list({c.get("label", {}).get("eng") for c in concepts if c.get("label")})[:12]

        current_url = request.build_absolute_uri()

        return {
            "article": article,
            "source": source,
            "categories": categories,
            "primary_category": primary_category,
            "concepts": concepts,
            "location": location,
            "gallery": gallery,
            "sentiment": sentiment,
            "reading_time": estimate_reading_time(body),
            "related_articles": related_articles,
            "latest_articles": latest_articles,
            "trending_articles": trending_articles,
            "prev_article": prev_article,
            "next_article": next_article,
            "popular_tags": popular_tags,
            "current_url": current_url,
        }


def news_404_view(request, exception=None):
    """
    Custom 404 handler. Wire this up in your root urls.py:
        handler404 = "news.views.news_404_view"
    """
    return render(request, "404.html", status=404)