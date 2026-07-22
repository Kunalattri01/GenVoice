from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from taxonomy.models import Tags


class TagsView(View):

    def get(self, request):
        context = {
            "report_data": Tags.objects.all(),
        }
        return render(request, "admin/taxonomy/tags.html", context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "create":
            return self._create(request)

        tag_id = request.POST.get("tag_id")
        if not tag_id:
            messages.error(request, "Missing tag reference.")
            return redirect("TagsPage")

        tag = get_object_or_404(Tags, pk=tag_id)

        if action == "update":
            return self._update(request, tag)
        elif action == "delete":
            return self._soft_delete(request, tag)

        messages.error(request, "Invalid action requested.")
        return redirect("TagsPage")

    # ---------- helpers ----------

    def _get_form_data(self, request):
        return {
            "name": request.POST.get("name", "").strip(),
            "is_active": request.POST.get("status") == "Active",
        }

    # ---------- actions ----------

    def _create(self, request):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Tag name is required.")
            return redirect("TagsPage")

        if Tags.objects.filter(name__iexact=data["name"]).exists():
            messages.error(request, "Tag with this name already exists.")
            return redirect("TagsPage")

        Tags.objects.create(
            name=data["name"],
            is_active=data["is_active"],
            entry_by=request.user,
        )

        messages.success(request, "Tag created successfully.")
        return redirect("TagsPage")

    def _update(self, request, tag):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Tag name is required.")
            return redirect("TagsPage")

        if Tags.objects.filter(name__iexact=data["name"]).exclude(pk=tag.pk).exists():
            messages.error(request, "Tag with this name already exists.")
            return redirect("TagsPage")

        tag.name = data["name"]
        tag.is_active = data["is_active"]
        tag.updated_by = request.user
        tag.save()

        messages.success(request, "Tag updated successfully.")
        return redirect("TagsPage")

    def _soft_delete(self, request, tag):
        """Soft delete: mark inactive instead of removing the row."""
        tag.is_active = False
        tag.updated_by = request.user
        tag.save(update_fields=["is_active", "updated_by", "updated_on"])

        messages.success(request, "Tag deleted successfully.")
        return redirect("TagsPage")