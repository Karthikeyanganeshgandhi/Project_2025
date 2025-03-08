from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def price(request):
    template = loader.get_template('pricing.html')
    return HttpResponse(template.render())


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
                return redirect('price')
            else:
                messages.error(request,'Invalid email or Password')
    else:
        form = signform()
    return render(request, 'index.html', {'form':form})

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

@login_required
def account(request):
    return render(request, 'Account.html', {'user':request.user})

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


def coursedet(request):
    template = loader.get_template('course-details.html')
    return HttpResponse(template.render())

@login_required
def courses(request):
    template = loader.get_template('courses.html')
    return HttpResponse(template.render())

def event(request):
    template = loader.get_template('events.html')
    return HttpResponse(template.render())

def ml(request):
    template = loader.get_template('ml.html')
    return HttpResponse(template.render())

@login_required
def progress(request):
    template = loader.get_template('progress.html')
    return HttpResponse(template.render())


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
    
    


def subscription(request):
    template = loader.get_template('subscription_details.html')
    return HttpResponse(template.render())

def trainers(request):
    template = loader.get_template('trainers.html')
    return HttpResponse(template.render())

def web(request):
    template = loader.get_template('web.html')
    return HttpResponse(template.render())

def testsuccess(request):
    template = loader.get_template('test_success.html')
    return HttpResponse(template.render())



