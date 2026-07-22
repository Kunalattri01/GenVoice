from django.http import Http404
from django.shortcuts import render
from django.views import View

from articles.models import Article


class NewsDetailView(View):
    """
    Renders the full detail page for a single Article.

    URL:     /news/<slug>/
    Example: /news/markets-rally-inflation-cools/
    """
    template_name = "UserInterface/news_detail.html"

    def get(self, request, slug, *args, **kwargs):
        article = (
            Article.objects.select_related("category", "source")
            .prefetch_related("authors", "tags", "gallery_images", "related_articles")
            .filter(slug=slug, status=Article.Status.PUBLISHED, is_active=True)
            .first()
        )

        if not article:
            raise Http404("This article could not be found or is no longer available.")

        # Lightweight view count increment (avoids re-running save() side effects)
        Article.objects.filter(pk=article.pk).update(view_count=article.view_count + 1)

        context = self._build_context(article, request)
        return render(request, self.template_name, context)

    def _build_context(self, article, request):
        gallery = []
        if article.featured_image:
            gallery.append(article.featured_image.url)
        for img in article.gallery_images.all():
            gallery.append(img.image.url)

        related_articles = list(
            article.related_articles.filter(status=Article.Status.PUBLISHED, is_active=True)[:4]
        )
        if not related_articles:
            related_articles = list(
                Article.objects.filter(
                    category=article.category, status=Article.Status.PUBLISHED, is_active=True
                )
                .exclude(pk=article.pk)
                .order_by("-publish_date")[:4]
            )

        latest_articles = (
            Article.objects.filter(status=Article.Status.PUBLISHED, is_active=True)
            .exclude(pk=article.pk)
            .order_by("-publish_date")[:5]
        )

        trending_articles = (
            Article.objects.filter(
                status=Article.Status.PUBLISHED, is_active=True, is_trending=True
            )
            .exclude(pk=article.pk)
            .order_by("-publish_date")[:5]
        )

        prev_article = (
            Article.objects.filter(
                status=Article.Status.PUBLISHED, is_active=True, publish_date__lt=article.publish_date
            )
            .order_by("-publish_date")
            .first()
        )

        next_article = (
            Article.objects.filter(
                status=Article.Status.PUBLISHED, is_active=True, publish_date__gt=article.publish_date
            )
            .order_by("publish_date")
            .first()
        )

        popular_tags = [tag.name for tag in article.tags.all()][:12]
        current_url = request.build_absolute_uri()

        return {
            "article": article,
            "source": article.source,
            "primary_category": article.category,
            "categories": [article.category] if article.category else [],
            "gallery": gallery,
            "reading_time": article.reading_time,
            "related_articles": related_articles,
            "latest_articles": latest_articles,
            "trending_articles": trending_articles,
            "prev_article": prev_article,
            "next_article": next_article,
            "popular_tags": popular_tags,
            "current_url": current_url,
        }


def news_404_view(request, exception=None):
    return render(request, "404.html", status=404)