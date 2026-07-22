from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from articles.models import Author


class AuthorsView(View):

    def get(self, request):
        context = {
            "report_data": Author.objects.all(),
        }
        return render(request, "admin/authors/authors.html", context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "create":
            return self._create(request)

        author_id = request.POST.get("author_id")
        if not author_id:
            messages.error(request, "Missing author reference.")
            return redirect("AuthorsPage")

        author = get_object_or_404(Author, pk=author_id)

        if action == "update":
            return self._update(request, author)
        elif action == "delete":
            return self._soft_delete(request, author)

        messages.error(request, "Invalid action requested.")
        return redirect("AuthorsPage")

    # ---------- helpers ----------

    def _get_form_data(self, request):
        return {
            "name": request.POST.get("name", "").strip(),
            "designation": request.POST.get("designation", "").strip(),
            "bio": request.POST.get("bio", "").strip(),
            "twitter_url": request.POST.get("twitter_url", "").strip(),
            "facebook_url": request.POST.get("facebook_url", "").strip(),
            "linkedin_url": request.POST.get("linkedin_url", "").strip(),
            "is_active": request.POST.get("status") == "Active",
        }

    # ---------- actions ----------

    def _create(self, request):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Author name is required.")
            return redirect("AuthorsPage")

        if Author.objects.filter(name__iexact=data["name"]).exists():
            messages.error(request, "Author with this name already exists.")
            return redirect("AuthorsPage")

        author = Author(
            name=data["name"],
            designation=data["designation"],
            bio=data["bio"],
            twitter_url=data["twitter_url"],
            facebook_url=data["facebook_url"],
            linkedin_url=data["linkedin_url"],
            is_active=data["is_active"],
            entry_by=request.user,
        )

        if request.FILES.get("avatar"):
            author.avatar = request.FILES["avatar"]

        author.save()

        messages.success(request, "Author created successfully.")
        return redirect("AuthorsPage")

    def _update(self, request, author):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Author name is required.")
            return redirect("AuthorsPage")

        if Author.objects.filter(name__iexact=data["name"]).exclude(pk=author.pk).exists():
            messages.error(request, "Author with this name already exists.")
            return redirect("AuthorsPage")

        author.name = data["name"]
        author.designation = data["designation"]
        author.bio = data["bio"]
        author.twitter_url = data["twitter_url"]
        author.facebook_url = data["facebook_url"]
        author.linkedin_url = data["linkedin_url"]
        author.is_active = data["is_active"]
        author.updated_by = request.user

        if request.FILES.get("avatar"):
            author.avatar = request.FILES["avatar"]

        author.save()

        messages.success(request, "Author updated successfully.")
        return redirect("AuthorsPage")

    def _soft_delete(self, request, author):
        """Soft delete: mark inactive instead of removing the row."""
        author.is_active = False
        author.updated_by = request.user
        author.save(update_fields=["is_active", "updated_by", "updated_on"])

        messages.success(request, "Author deleted successfully.")
        return redirect("AuthorsPage")