from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# =========================================================================================================================================================================================================================

class registerform(forms.Form):
    full_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=15, required=True)
    email =  forms.EmailField(max_length=200, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

# =============================================================================================================================================================================================================================

class signform(forms.Form):
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# ===============================================================================================================================================================================================================================

class SkillTesterForm(forms.Form):
    question1 = forms.MultipleChoiceField(
        choices=[('Option 1', 'Option 1'), ('Option 2', 'Option 2'), ('Option 3', 'Option 3')],
        widget=forms.CheckboxSelectMultiple,
        label="1. What is the Answer?"
    )
    question2 = forms.MultipleChoiceField(
        choices=[('Option 1', 'Option 1'), ('Option 2', 'Option 2'), ('Option 3', 'Option 3')],
        widget=forms.CheckboxSelectMultiple,
        label="2. Choose the correct answers"
    )
    question3 = forms.ChoiceField(
        choices=[('Option A', 'Option A'), ('Option B', 'Option B'), ('Option C', 'Option C')],
        widget=forms.RadioSelect,
        label="3. Select the correct option"
    )
    question4 = forms.MultipleChoiceField(
        choices=[('Option 1', 'Option 1'), ('Option 2', 'Option 2'), ('Option 3', 'Option 3')],
        widget=forms.CheckboxSelectMultiple,
        label="4. Choose the correct answers"
    )
    question5 = forms.ChoiceField(
        choices=[('Option A', 'Option A'), ('Option B', 'Option B'), ('Option C', 'Option C')],
        widget=forms.RadioSelect,
        label="5. Select the correct option"
    )

# ===================================================================================================================================================================================================================================

from .models import contactdetail

class contactform(forms.ModelForm):
    class Meta:
        model=contactdetail
        fields=['name','email','subject','message']

# ======================================================================================================================================================================================================================================