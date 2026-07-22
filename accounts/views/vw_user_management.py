from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

User = get_user_model()


class UserManagementView(View):

    def get(self, request):
        users_qs = User.objects.all()

        paginator = Paginator(users_qs, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "roles": User.ROLE_CHOICES,
            "pagination": True
        }
        return render(request, "admin/users/user_management.html", context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "create":
            return self._create(request)

        user_id = request.POST.get("user_id")
        if not user_id:
            messages.error(request, "Missing user reference.")
            return redirect("UserManagementPage")

        target_user = get_object_or_404(User, pk=user_id)

        if action == "update":
            return self._update(request, target_user)
        elif action == "delete":
            return self._deactivate(request, target_user)

        messages.error(request, "Invalid action requested.")
        return redirect("UserManagementPage")

    # ---------- helpers ----------

    def _get_form_data(self, request):
        return {
            "full_name": request.POST.get("full_name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "role": request.POST.get("role", "").strip(),
            "is_active": request.POST.get("status") == "Active",
            "password": request.POST.get("password", "").strip(),
        }

    def _split_name(self, full_name):
        parts = full_name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
        return first_name, last_name

    # ---------- actions ----------

    def _create(self, request):
        data = self._get_form_data(request)

        if not data["full_name"]:
            messages.error(request, "Full name is required.")
            return redirect("UserManagementPage")

        if not data["email"]:
            messages.error(request, "Email address is required.")
            return redirect("UserManagementPage")

        if User.objects.filter(email__iexact=data["email"]).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect("UserManagementPage")

        if not data["password"]:
            messages.error(request, "A temporary password is required.")
            return redirect("UserManagementPage")

        if len(data["password"]) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("UserManagementPage")

        if data["role"] not in dict(User.ROLE_CHOICES):
            messages.error(request, "Please select a valid role.")
            return redirect("UserManagementPage")

        first_name, last_name = self._split_name(data["full_name"])

        new_user = User(
            username=data["email"],
            email=data["email"],
            first_name=first_name,
            last_name=last_name,
            role=data["role"],
            is_active=data["is_active"],
        )
        new_user.set_password(data["password"])
        new_user.save()

        messages.success(request, f"User \"{data['full_name']}\" created successfully.")
        return redirect("UserManagementPage")

    def _update(self, request, target_user):
        data = self._get_form_data(request)

        if not data["full_name"]:
            messages.error(request, "Full name is required.")
            return redirect("UserManagementPage")

        if not data["email"]:
            messages.error(request, "Email address is required.")
            return redirect("UserManagementPage")

        if User.objects.filter(email__iexact=data["email"]).exclude(pk=target_user.pk).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect("UserManagementPage")

        if data["role"] not in dict(User.ROLE_CHOICES):
            messages.error(request, "Please select a valid role.")
            return redirect("UserManagementPage")

        # Prevent an admin from locking themselves out by deactivating their own account
        if target_user.pk == request.user.pk and not data["is_active"]:
            messages.error(request, "You can't deactivate your own account.")
            return redirect("UserManagementPage")

        first_name, last_name = self._split_name(data["full_name"])

        target_user.first_name = first_name
        target_user.last_name = last_name
        target_user.email = data["email"]
        target_user.username = data["email"]
        target_user.role = data["role"]
        target_user.is_active = data["is_active"]

        if data["password"]:
            if len(data["password"]) < 8:
                messages.error(request, "New password must be at least 8 characters long.")
                return redirect("UserManagementPage")
            target_user.set_password(data["password"])

        target_user.save()

        messages.success(request, "User updated successfully.")
        return redirect("UserManagementPage")

    def _deactivate(self, request, target_user):
        if target_user.pk == request.user.pk:
            messages.error(request, "You can't delete your own account.")
            return redirect("UserManagementPage")

        target_user.is_active = False
        target_user.save(update_fields=["is_active"])

        messages.success(request, "User deactivated successfully.")
        return redirect("UserManagementPage")