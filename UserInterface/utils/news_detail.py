"""
news/utils.py

Thin wrapper around the Event Registry REST API.
No database models are used anywhere in this module — every call goes
straight to Event Registry, on every request.

Add to settings.py:
    EVENT_REGISTRY_API_KEY = "xxxxxxxxxxxxxxxxxxxx"
    EVENT_REGISTRY_TIMEOUT = 10   # seconds, optional
"""

import logging
import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

ARTICLE_URL = "https://eventregistry.org/api/v1/article/getArticle"
ARTICLES_URL = "https://eventregistry.org/api/v1/article/getArticles"

DEFAULT_TIMEOUT = getattr(settings, "EVENT_REGISTRY_TIMEOUT", 10)


def _api_key():
    return settings.EVENT_REGISTRY_API_KEY


def fetch_article_by_uri(article_uri, use_cache=True, cache_seconds=300):
    """
    Fetch the FULL article object for a single article URI.

    Returns a dict (the article's "info" object) or None if the article
    could not be found / an error occurred.
    """
    if not article_uri:
        return None

    cache_key = f"er_article_detail:{article_uri}"
    if use_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    params = {
        "action": "getArticle",
        "articleUri": article_uri,
        "resultType": "info",
        "apiKey": _api_key(),
        "infoArticleBodyLen": -1,          # -1 = full body, not truncated
        "includeArticleConcepts": True,
        "includeArticleCategories": True,
        "includeArticleLinks": True,
        "includeArticleVideos": True,
        "includeArticleImage": True,
        "includeArticleSocialScore": True,
        "includeArticleSentiment": True,
        "includeArticleLocation": True,
        "includeArticleExtractedDates": True,
        "includeArticleOriginalArticle": True,
        "includeSourceTitle": True,
        "includeSourceDescription": False,
        "includeSourceLocation": True,
        "includeSourceRanking": False,
        "includeConceptImage": True,
        "includeConceptDescription": False,
        "includeCategoryParentUri": True,
    }

    try:
        response = requests.get(ARTICLE_URL, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.error("Event Registry getArticle failed for uri=%s: %s", article_uri, exc)
        return None

    # Event Registry keys the response by the article URI you asked for.
    article_wrapper = data.get(article_uri)
    if not article_wrapper:
        logger.warning("Event Registry returned no data for uri=%s", article_uri)
        return None

    info = article_wrapper.get("info")
    if not info:
        error_msg = article_wrapper.get("error")
        if error_msg:
            logger.warning("Event Registry error for uri=%s: %s", article_uri, error_msg)
        return None

    if use_cache:
        cache.set(cache_key, info, cache_seconds)

    return info


def search_articles(extra_params=None, count=6, sort_by="date"):
    """
    Generic search against Event Registry's getArticles endpoint.
    Used for "Latest News", "Trending News", "Related Articles",
    and Previous/Next lookups. Returns a list of article dicts
    (never raises — returns [] on any failure).
    """
    params = {
        "action": "getArticles",
        "resultType": "articles",
        "articlesSortBy": sort_by,          # date | socialScore | rel
        "articlesCount": count,
        "articlesArticleBodyLen": 300,
        "includeArticleImage": True,
        "includeArticleConcepts": False,
        "includeArticleCategories": True,
        "includeSourceTitle": True,
        "apiKey": _api_key(),
        "lang": "eng",
    }
    if extra_params:
        params.update(extra_params)

    try:
        response = requests.get(ARTICLES_URL, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.error("Event Registry getArticles failed: %s", exc)
        return []

    results = data.get("articles", {}).get("results", [])
    return results


def get_related_articles(article, count=4):
    """Articles sharing the same primary category, excluding the current one."""
    categories = article.get("categories") or []
    category_uri = categories[0].get("uri") if categories else None
    if not category_uri:
        return []

    results = search_articles(
        {"categoryUri": category_uri, "articlesSortBy": "date"},
        count=count + 1,
    )
    return [a for a in results if a.get("uri") != article.get("uri")][:count]


def get_latest_articles(exclude_uri=None, count=5):
    results = search_articles({"articlesSortBy": "date"}, count=count + 1)
    return [a for a in results if a.get("uri") != exclude_uri][:count]


def get_trending_articles(exclude_uri=None, count=5):
    results = search_articles({"articlesSortBy": "socialScore"}, count=count + 1)
    return [a for a in results if a.get("uri") != exclude_uri][:count]


def get_prev_next_articles(article):
    """
    Best-effort "Previous / Next" navigation: pulls the two articles from
    the same source published immediately before / after this one.
    """
    source_uri = (article.get("source") or {}).get("uri")
    published = article.get("dateTimePub") or article.get("dateTime")
    if not source_uri or not published:
        return None, None

    date_only = published.split("T")[0]

    older = search_articles(
        {
            "sourceUri": source_uri,
            "dateEnd": date_only,
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
        },
        count=5,
    )
    newer = search_articles(
        {
            "sourceUri": source_uri,
            "dateStart": date_only,
            "articlesSortBy": "date",
            "articlesSortByAsc": True,
        },
        count=5,
    )

    prev_article = next((a for a in older if a.get("uri") != article.get("uri")), None)
    next_article = next((a for a in newer if a.get("uri") != article.get("uri")), None)
    return prev_article, next_article


def estimate_reading_time(body_text, words_per_minute=200):
    if not body_text:
        return 1
    word_count = len(body_text.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes