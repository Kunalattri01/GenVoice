from accounts.models import User


def login_details(request):
    if request.user.is_authenticated:
        user = request.user

        return {
            "login_user": user,
            "login_user_name": user.get_full_name() or user.username,
            "login_user_role": user.role,
            "login_user_image": user.profile_image,
        }

    return {
        "login_user": None,
        "login_user_name": "",
        "login_user_role": "",
        "login_user_image": None,
    }