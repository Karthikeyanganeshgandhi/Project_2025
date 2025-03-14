from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Subsc

class SubscriptionRequiredMiddleware:
   

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            active_subscription = Subsc.objects.filter(user=request.user, status="active").exists()

            # Check if the user is visiting a restricted page without an active subscription
            restricted_paths = ["/coursedet/","/ml/","/web/"]  # Add restricted pages
            if request.path in restricted_paths and not active_subscription:
                return redirect('price')  # Redirect to subscription page

        return self.get_response(request)
