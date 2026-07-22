from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from articles.models import Source


class SourcesView(View):
    
    def get(self, request):
        context = {
            "report_data": Source.objects.all(),
        }
        return render(request, "admin/sources/sources.html", context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "create":
            return self._create(request)

        source_id = request.POST.get("source_id")
        if not source_id:
            messages.error(request, "Missing source reference.")
            return redirect("SourcesPage")

        source = get_object_or_404(Source, pk=source_id)

        if action == "update":
            return self._update(request, source)
        elif action == "delete":
            return self._soft_delete(request, source)

        messages.error(request, "Invalid action requested.")
        return redirect("SourcesPage")

    # ---------- helpers ----------

    def _get_form_data(self, request):
        return {
            "name": request.POST.get("name", "").strip(),
            "url": request.POST.get("url", "").strip(),
            "is_active": request.POST.get("status") == "Active",
        }

    # ---------- actions ----------

    def _create(self, request):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Source name is required.")
            return redirect("SourcesPage")

        if Source.objects.filter(name__iexact=data["name"]).exists():
            messages.error(request, "Source with this name already exists.")
            return redirect("SourcesPage")

        source = Source(
            name=data["name"],
            url=data["url"],
            is_active=data["is_active"],
            entry_by=request.user,
        )

        if request.FILES.get("logo"):
            source.logo = request.FILES["logo"]

        source.save()

        messages.success(request, "Source created successfully.")
        return redirect("SourcesPage")

    def _update(self, request, source):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Source name is required.")
            return redirect("SourcesPage")

        if Source.objects.filter(name__iexact=data["name"]).exclude(pk=source.pk).exists():
            messages.error(request, "Source with this name already exists.")
            return redirect("SourcesPage")

        source.name = data["name"]
        source.url = data["url"]
        source.is_active = data["is_active"]
        source.updated_by = request.user

        if request.FILES.get("logo"):
            source.logo = request.FILES["logo"]

        source.save()

        messages.success(request, "Source updated successfully.")
        return redirect("SourcesPage")

    def _soft_delete(self, request, source):
        """Soft delete: mark inactive instead of removing the row."""
        source.is_active = False
        source.updated_by = request.user
        source.save(update_fields=["is_active", "updated_by", "updated_on"])

        messages.success(request, "Source deleted successfully.")
        return redirect("SourcesPage")