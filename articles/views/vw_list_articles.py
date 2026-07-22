from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from taxonomy.models import Categories
from articles.models import Article


class ListArticlesView(View):

    def get(self, request):

        context = {
            "report_data": Article.objects.select_related("category").prefetch_related("authors"),
            "categories": Categories.objects.filter(is_active=True),
            "statuses": Article.Status.choices,
        }
        return render(request, "admin/articles/list_articles.html", context)
    

    def post(self, request):
        action = request.POST.get("action")

        article_id = request.POST.get("article_id")

        if not article_id:
            messages.error(request, "Missing article reference.")
            return redirect("ListArticlesPage")

        article = get_object_or_404(Article, pk=article_id)

        if action == "delete":
            return self._soft_delete(request, article)

        messages.error(request, "Invalid action requested.")
        return redirect("ListArticlesPage")

    def _soft_delete(self, request, article):
        """Soft delete: mark inactive instead of removing the row."""
        article.is_active = False
        article.updated_by = request.user
        article.save(update_fields=["is_active", "updated_by", "updated_on"])

        messages.success(request, "Article deleted successfully.")
        return redirect("ListArticlesPage")