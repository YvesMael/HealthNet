from .models import Hospital, ServicesInHospital, Autorisation
from django import forms
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class HospitalSignInForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name','phone_number','email','location']
    
class ServicesInHospitalForm(forms.ModelForm):
    class Meta:
        model = ServicesInHospital
        fields = ['number_of_beds','phone_number','email']
    
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder':'Entrer votre username'}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Entrer votre prenom','label':'First Name'}))
    last_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder':'Entrer votre nom de famille','label':'Last Name'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}))
    sex = forms.RadioSelect()
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder':'examplexyz@gmail.com'}))
    religion = forms.Select()
    blood_group = forms.Select()
    city = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Entrer votre ville'}))


    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username','first_name','last_name','sex','date_of_birth','created_at','email','phone_number','religion','blood_group','city','occupation','numero_carte_biometrique','quarter','allergy','marital_status','nationality']

class VerificationForm(forms.Form):
    code = forms.CharField(max_length=15, required=True)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profil','username','first_name','last_name','sex','date_of_birth','phone_number','email','created_at','city','religion','occupation','allergy')
        widgets = {
            'username': forms.TextInput(attrs={'readonly':'readonly'}),
            'sex': forms.TextInput(attrs={'readonly':'readonly'}),
            'date_of_birth': forms.DateInput(attrs={'readonly':'readonly'}),
            'created_at': forms.TextInput(attrs={'readonly':'readonly'}),
        }

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password','palceholder':'Currents password', 'id':'old_password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'type':'password', 'palceholder':'Newwd password','id':'new_password1'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'type':'password', 'palceholder':'Confirm password', 'id':'new_password2'}))

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1','new_password2')


class ForgotPasswordForm(forms.Form):
    class Meta:
        model = get_user_model()
        fields = ('username','email')
    
class ResetPasswordForm(forms.Form):
    id = forms.CharField(max_length=24, widget=forms.HiddenInput(attrs={'id':'id'}))
    token = forms.CharField(max_length=74, widget=forms.HiddenInput(attrs={'id':'token'}))
    new_password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'type':'password','id':'new_password1'}))
    new_password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'type':'password','id':'new_password2'}))

class AutorisationForm(forms.ModelForm):
    class Meta:
        model = Autorisation
        fields = "__all__"