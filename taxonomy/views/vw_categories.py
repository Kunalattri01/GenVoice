from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from taxonomy.models import Categories


class CategoriesView(View):

    def get(self, request):
        context = {
            "report_data": Categories.objects.all(),
            "search_indices": list(range(7)),
        }
        return render(request, "admin/taxonomy/categories.html", context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "create":
            return self._create(request)

        category_id = request.POST.get("category_id")
        if not category_id:
            messages.error(request, "Missing category reference.")
            return redirect("CategoriesPage")

        category = get_object_or_404(Categories, pk=category_id)

        if action == "update":
            return self._update(request, category)
        elif action == "delete":
            return self._soft_delete(request, category)

        messages.error(request, "Invalid action requested.")
        return redirect("CategoriesPage")

    # ---------- helpers ----------

    def _get_form_data(self, request):
        return {
            "name": request.POST.get("name", "").strip(),
            "description": request.POST.get("description", "").strip(),
            "icon": request.POST.get("category_icon", "").strip(),
            "icon_color": request.POST.get("icon_color", "").strip() or "text-textsecondary",
            "display_order": request.POST.get("display_order") or 0,
            "is_active": request.POST.get("status") == "Active",
        }

    # ---------- actions ----------

    def _create(self, request):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Category name is required.")
            return redirect("CategoriesPage")

        if Categories.objects.filter(name__iexact=data["name"]).exists():
            messages.error(request, "Category with this name already exists.")
            return redirect("CategoriesPage")

        Categories.objects.create(
            name=data["name"],
            description=data["description"],
            icon=data["icon"],
            icon_color=data["icon_color"],
            display_order=data["display_order"],
            is_active=data["is_active"],
            entry_by=request.user,
        )

        messages.success(request, "Category created successfully.")
        return redirect("CategoriesPage")

    def _update(self, request, category):
        data = self._get_form_data(request)

        if not data["name"]:
            messages.error(request, "Category name is required.")
            return redirect("CategoriesPage")

        if Categories.objects.filter(name__iexact=data["name"]).exclude(pk=category.pk).exists():
            messages.error(request, "Category with this name already exists.")
            return redirect("CategoriesPage")

        category.name = data["name"]
        category.description = data["description"]
        category.icon = data["icon"]
        category.icon_color = data["icon_color"]
        category.display_order = data["display_order"]
        category.is_active = data["is_active"]
        category.updated_by = request.user
        category.save()

        messages.success(request, "Category updated successfully.")
        return redirect("CategoriesPage")

    def _soft_delete(self, request, category):
        """Soft delete: mark inactive instead of removing the row."""
        category.is_active = False
        category.updated_by = request.user
        category.save(update_fields=["is_active", "updated_by", "updated_on"])

        messages.success(request, "Category deleted successfully.")
        return redirect("CategoriesPage")