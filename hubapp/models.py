from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# =================================================================================================================================================

class contactdetail(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=170)
    subject=models.CharField(max_length=400)
    message=models.TextField()

    def __str__(self):
        return self.name
    
# ================================================================================================================================================
    
from django.db import models
from django.contrib.auth.models import User

class Subsc(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('expired', 'Expired')], default='active')
    active = models.BooleanField(default=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
    
# ====================================================================================================================================================
