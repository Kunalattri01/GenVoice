from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from taxonomy.models import Categories, Tags
from articles.models import Article, ArticleImage, Author, Source

class ManageArticlesView(View):

    def get(self, request):
        article_id = request.GET.get("article_id")
        article = None

        if article_id:
            article = get_object_or_404(Article, pk=article_id)

        context = {
            "article": article,
            "categories": Categories.objects.filter(is_active=True),
            "tags": Tags.objects.filter(is_active=True),
            "authors": Author.objects.filter(is_active=True),
            "sources": Source.objects.filter(is_active=True),
            "pagination": True,
        }
        return render(request, "admin/articles/manage_articles.html", context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "create":
            return self._create(request)
        elif action == "update":
            return self._update(request)

        messages.error(request, "Invalid action requested.")
        return redirect("ManageArticlesPage")

    # ---------- helpers ----------

    def _get_form_data(self, request):
        return {
            "title": request.POST.get("title", "").strip(),
            "short_description": request.POST.get("short_description", "").strip(),
            "content": request.POST.get("content", "").strip(),
            "category_id": request.POST.get("category") or None,
            "source_id": request.POST.get("source") or None,
            "status": request.POST.get("status") or Article.Status.DRAFT,
            "publish_date": request.POST.get("publish_date") or None,
            "is_featured": request.POST.get("is_featured") == "true",
            "is_breaking_news": request.POST.get("is_breaking_news") == "true",
            "is_trending": request.POST.get("is_trending") == "true",
            "is_editors_pick": request.POST.get("is_editors_pick") == "true",
            "seo_title": request.POST.get("seo_title", "").strip(),
            "seo_description": request.POST.get("seo_description", "").strip(),
            "focus_keyword": request.POST.get("focus_keyword", "").strip(),
            "canonical_url": request.POST.get("canonical_url", "").strip(),
            "tag_ids": request.POST.getlist("tags"),
            "author_ids": request.POST.getlist("authors"),
        }

    def _apply_files(self, article, request):
        if request.FILES.get("featured_image"):
            article.featured_image = request.FILES["featured_image"]
        if request.FILES.get("og_image"):
            article.og_image = request.FILES["og_image"]
        if request.FILES.get("twitter_image"):
            article.twitter_image = request.FILES["twitter_image"]

    def _apply_gallery_images(self, article, request):
        """Any newly uploaded gallery images are appended (existing ones are untouched)."""
        gallery_files = request.FILES.getlist("gallery_images")
        existing_count = article.gallery_images.count()

        for index, file in enumerate(gallery_files):
            ArticleImage.objects.create(
                article=article,
                image=file,
                display_order=existing_count + index,
                entry_by=request.user,
            )

    def _manage_url(self, article_id=None):
        url = reverse("ManageArticlesPage")
        return f"{url}?article_id={article_id}" if article_id else url

    # ---------- actions ----------

    def _create(self, request):
        data = self._get_form_data(request)

        if not data["title"]:
            messages.error(request, "Headline is required.")
            return redirect(self._manage_url())

        if not data["category_id"]:
            messages.error(request, "Category is required.")
            return redirect(self._manage_url())

        article = Article(
            title=data["title"],
            short_description=data["short_description"],
            content=data["content"],
            category_id=data["category_id"],
            source_id=data["source_id"],
            status=data["status"],
            publish_date=data["publish_date"] or None,
            is_featured=data["is_featured"],
            is_breaking_news=data["is_breaking_news"],
            is_trending=data["is_trending"],
            is_editors_pick=data["is_editors_pick"],
            seo_title=data["seo_title"],
            seo_description=data["seo_description"],
            focus_keyword=data["focus_keyword"],
            canonical_url=data["canonical_url"],
            entry_by=request.user,
        )

        self._apply_files(article, request)
        article.save()

        article.tags.set(data["tag_ids"])
        article.authors.set(data["author_ids"])
        self._apply_gallery_images(article, request)

        messages.success(request, "Article created successfully.")
        return redirect("ListArticlesPage")

    def _update(self, request):
        article_id = request.POST.get("article_id")
        if not article_id:
            messages.error(request, "Missing article reference.")
            return redirect("ListArticlesPage")

        article = get_object_or_404(Article, pk=article_id)
        data = self._get_form_data(request)

        if not data["title"]:
            messages.error(request, "Headline is required.")
            return redirect(self._manage_url(article_id))

        if not data["category_id"]:
            messages.error(request, "Category is required.")
            return redirect(self._manage_url(article_id))

        article.title = data["title"]
        article.short_description = data["short_description"]
        article.content = data["content"]
        article.category_id = data["category_id"]
        article.source_id = data["source_id"]
        article.status = data["status"]
        article.publish_date = data["publish_date"] or None
        article.is_featured = data["is_featured"]
        article.is_breaking_news = data["is_breaking_news"]
        article.is_trending = data["is_trending"]
        article.is_editors_pick = data["is_editors_pick"]
        article.seo_title = data["seo_title"]
        article.seo_description = data["seo_description"]
        article.focus_keyword = data["focus_keyword"]
        article.canonical_url = data["canonical_url"]
        article.updated_by = request.user

        self._apply_files(article, request)
        article.save()

        article.tags.set(data["tag_ids"])
        article.authors.set(data["author_ids"])
        self._apply_gallery_images(article, request)

        messages.success(request, "Article updated successfully.")
        return redirect("ListArticlesPage")