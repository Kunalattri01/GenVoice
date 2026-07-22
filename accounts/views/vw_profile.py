from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from django.views import View


class ProfileView(View):

    def get(self, request):
        context = {
            'pagination' : True
        }
        return render(request, "admin/profile/profile.html", context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "update_profile":
            return self._update_profile(request)
        elif action == "change_password":
            return self._change_password(request)

        messages.error(request, "Invalid action requested.")
        return redirect("ProfilePage")


    # ---------- actions ----------
    def _update_profile(self, request):
        user = request.user

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()

        if not full_name:
            messages.error(request, "Full name is required.")
            return redirect("ProfilePage")

        if not email:
            messages.error(request, "Email is required.")
            return redirect("ProfilePage")

        name_parts = full_name.split(" ", 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        user.email = email
        user.phone_number = phone_number

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES["profile_image"]

        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("ProfilePage")

    def _change_password(self, request):
        user = request.user

        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("ProfilePage")

        if not new_password:
            messages.error(request, "New password is required.")
            return redirect("ProfilePage")

        if len(new_password) < 8:
            messages.error(request, "New password must be at least 8 characters long.")
            return redirect("ProfilePage")

        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect("ProfilePage")

        user.set_password(new_password)
        user.save()

        # Keeps the user logged in after changing their own password
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully.")
        return redirect("ProfilePage")