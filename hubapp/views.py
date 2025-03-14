from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import subscription_required

# ===============================================================================================================================================================

# Create your views here.




from .forms import signform

def index(request):
    if request.method == 'POST':
        form = signform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('courses')
            else:
                messages.error(request,'Invalid email or Password')
    else:
        form = signform()
    return render(request, 'index.html', {'form':form})

# ================================================================================================================================================================

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

# ==================================================================================================================================================================

@login_required
def account(request):
    return render(request, 'Account.html', {'user':request.user})

# ===================================================================================================================================================================

from .models import contactdetail
from .forms import contactform

def contact(request):
    if request.method == 'POST':
        form = contactform(request.POST)
        if form.is_valid():
                form.save()
                return redirect('contacts')
               
    else:
        form=contactform()

    return render(request,'contact.html',{'form':form})

def contacts(request):
    det=contactdetail.objects.all()
    return render(request,'index.html',{'det':det})

# ===================================================================================================================================================================

@subscription_required
def coursedet(request):
    template = loader.get_template('course-details.html')
    return HttpResponse(template.render())

# ====================================================================================================================================================================

@login_required
def courses(request):
    template = loader.get_template('courses.html')
    return HttpResponse(template.render())

# =====================================================================================================================================================================

def event(request):
    template = loader.get_template('events.html')
    return HttpResponse(template.render())

# ======================================================================================================================================================================

@subscription_required
def ml(request):
    template = loader.get_template('ml.html')
    return HttpResponse(template.render())

# =======================================================================================================================================================================

@login_required
def progress(request):
    template = loader.get_template('progress.html')
    return HttpResponse(template.render())

# =========================================================================================================================================================================


from .forms import registerform  

def register(request):
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:

                user = User.objects.create_user(username=email, email=email, password=password1)
                user.first_name = full_name
                user.last_name = last_name
                user.save()

                messages.success(request, f'Account created for {full_name} {last_name}')
                return redirect('index')
            else:
                messages.error(request, 'passwords do not match')

    form = registerform()
    return render(request, 'register.html', {'form':form})

# ===========================================================================================================================================================================================


from .forms import SkillTesterForm

@login_required
def skilltester(request):
    if request.method == 'POST':
        form = SkillTesterForm(request.POST)
        if form.is_valid():
            # Process the form data
            answers = form.cleaned_data
            print("User Answers:", answers)  # You can save these answers or process them as needed
            return redirect('thank_you_view')  # Redirect to a "Thank You" page or any other page
    else:
        form = SkillTesterForm()
    
    return render(request, 'skilltester.html', {'form': form})
def thank_you_view(request):
    return render(request, 'test_success.html')

# ==================================================================================================================================================================================================
    
    


def subscription(request):
    template = loader.get_template('subscription_details.html')
    return HttpResponse(template.render())

# =======================================================================================================================================================================================================

def trainers(request):
    template = loader.get_template('trainers.html')
    return HttpResponse(template.render())

# ========================================================================================================================================================================================================

@subscription_required
def web(request):
    template = loader.get_template('web.html')
    return HttpResponse(template.render())

# ===========================================================================================================================================================================================================

def testsuccess(request):
    template = loader.get_template('test_success.html')
    return HttpResponse(template.render())

# =============================================================================================================================================================================================================


import razorpay
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Subsc
from django.shortcuts import get_object_or_404



# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Subscription plans with pricing in paise
amount_mapping = {
    "basic": 10000,    # ₹100
    "standard": 30000, # ₹300
    "premium": 50000,  # ₹500
    "annual": 500000,  # ₹5000
}

# 1️⃣ Render Subscription Page
def price(request):
    return render(request, "pricing.html")  # Ensure this template exists in `templates/`

# 2️⃣ Create Payment Order
def create_payment(request, plan):
    if plan not in amount_mapping:
        return JsonResponse({"error": "Invalid plan"}, status=400)

    try:
        payment_data = {
            "amount": amount_mapping[plan],  # Razorpay expects amount in paise
            "currency": "INR",
            "receipt": f"receipt_{plan}",
            "payment_capture": 1
        }

        order = client.order.create(data=payment_data)

        if "id" not in order:
            return JsonResponse({"error": "Failed to create order"}, status=500)

        # Save order details in subscription model
        subscription, created = Subsc.objects.get_or_create(user=request.user)
        subscription.razorpay_order_id = order["id"]
        subscription.status = "pending"
        subscription.save()

        return JsonResponse({"order_id": order["id"], "amount": order["amount"], "currency": "INR"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# 3️⃣ Verify Payment
@csrf_exempt
def verify_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)  # Read incoming JSON request

        # Debugging: Print received data in Django logs
        print("🔹 Received Payment Data:", data)

        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        # If any parameter is missing, return error
        if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
            return JsonResponse({"error": "Missing payment parameters", "received_data": data}, status=400)

        # Verify payment signature with Razorpay
        params_dict = {
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_order_id": razorpay_order_id,
            "razorpay_signature": razorpay_signature,
        }

        try:
            client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            print("❌ Signature verification failed!")
            return JsonResponse({"error": "Payment verification failed"}, status=400)

        # Update subscription status to "active"
        updated = Subsc.objects.filter(razorpay_order_id=razorpay_order_id).update(status="active")

        if updated:
            print("✅ Subscription activated!")
            return JsonResponse({"status": "success", "message": "Subscription activated"}, status=200)
        else:
            return JsonResponse({"error": "Subscription not found"}, status=404)

    except Exception as e:
        print("❌ Error in verify_payment:", str(e))  # Debugging
        return JsonResponse({"error": str(e)}, status=500)
    
# ==============================================================================================================================================================================================================
