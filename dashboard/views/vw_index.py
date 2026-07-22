from datetime import timedelta

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from articles.models import Article
from taxonomy.models import Categories

User = get_user_model()


class DashboardView(View):

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        prev_period_start = now - timedelta(days=60)

        articles_qs = Article.objects.filter(is_active=True)
        categories_qs = Categories.objects.filter(is_active=True)

        context = {
            "total_articles": articles_qs.count(),
            "published_count": articles_qs.filter(status=Article.Status.PUBLISHED).count(),
            "draft_count": articles_qs.filter(status=Article.Status.DRAFT).count(),
            "category_count": categories_qs.count(),

            "growth": self._growth_stats(articles_qs, categories_qs, now, thirty_days_ago, prev_period_start),

            "recent_articles": articles_qs.select_related("category")
                .prefetch_related("authors")
                .order_by("-entry_on")[:5],

            "recent_users": User.objects.order_by("-date_joined")[:5],
            'pagination' : True
        }

        return render(request, "admin/dashboard/index.html", context)

    def _growth_stats(self, articles_qs, categories_qs, now, thirty_days_ago, prev_period_start):
        """
        Compares the last 30 days against the 30 days before that.
        Returns percentage change (positive or negative) for each stat card.
        """
        def pct_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 1)

        articles_last_30 = articles_qs.filter(entry_on__gte=thirty_days_ago).count()
        articles_prev_30 = articles_qs.filter(
            entry_on__gte=prev_period_start, entry_on__lt=thirty_days_ago
        ).count()

        published_last_30 = articles_qs.filter(
            status=Article.Status.PUBLISHED, publish_date__gte=thirty_days_ago
        ).count()
        published_prev_30 = articles_qs.filter(
            status=Article.Status.PUBLISHED,
            publish_date__gte=prev_period_start,
            publish_date__lt=thirty_days_ago,
        ).count()

        draft_last_30 = articles_qs.filter(
            status=Article.Status.DRAFT, entry_on__gte=thirty_days_ago
        ).count()
        draft_prev_30 = articles_qs.filter(
            status=Article.Status.DRAFT,
            entry_on__gte=prev_period_start,
            entry_on__lt=thirty_days_ago,
        ).count()

        categories_last_30 = categories_qs.filter(entry_on__gte=thirty_days_ago).count()
        categories_prev_30 = categories_qs.filter(
            entry_on__gte=prev_period_start, entry_on__lt=thirty_days_ago
        ).count()

        return {
            "articles": pct_change(articles_last_30, articles_prev_30),
            "published": pct_change(published_last_30, published_prev_30),
            "drafts": pct_change(draft_last_30, draft_prev_30),
            "categories": pct_change(categories_last_30, categories_prev_30),
        }    

    def post(self, request):
        return redirect('DashboardPage')