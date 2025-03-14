from django.shortcuts import redirect
from .models import Subsc

def subscription_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            has_subscription = Subsc.objects.filter(user=request.user, status="active").exists()
            if not has_subscription:
                return redirect("price")  # Redirect if not subscribed
        else:
            return redirect("login")  # Redirect if not logged in

        return view_func(request, *args, **kwargs)
    return wrapper
