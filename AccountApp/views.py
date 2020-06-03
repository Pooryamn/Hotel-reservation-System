import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import authenticate,login
from django.urls import reverse
from .forms import LoginForm,UserRegistrationForm
from .models import Profile


# Create your views here.


def user_login(request):
    error = ""
    if (request.method == 'POST'):
        form = LoginForm(request.POST)

        if (form.is_valid()):
            cd = form.cleaned_data

            user = authenticate(username = cd['username'],password = cd['password'])

            if (user is not None):
                if user.is_active:
                    login(request,user)

                    return HttpResponse('Authenticated successfully !')
                
                else:
                    error = "حساب کاربری شما غیر فعال است."
            else:
                error = "نام کاربری یا رمز عبور اشتباه است."
    else:
        form = LoginForm()
        
    return render(request,'AccountApp/login.html',{'form':form, 'error':error})


def register(request):

    global user_form
    global new_user

    if (request.method == 'POST'):
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # create a new user
            new_user = user_form.save(commit=False)
            # set password:
            new_user.set_password(user_form.cleaned_data['password'])

            # create a password here
            GeneratedPass = PassGen()

            # send password to user email
            # email body
            Email_Body = 'Dear ' + user_form.cleaned_data['first_name']
            Email_Body += ' ' + user_form.cleaned_data['last_name']
            Email_Body += '\n\nYour Verification Code is '
            Email_Body += GeneratedPass

            # email subject 
            Email_Subject = 'Verify your account'
            
            # To :
            Email_reciver = [user_form.cleaned_data['email']]

            # main part of sending :
            send_mail(Email_Subject,Email_Body,settings.EMAIL_HOST_USER,Email_reciver,fail_silently=True)
            # open confrim page
            
            request.session['MainPass'] = GeneratedPass

            return render(request,'AccountApp/Confrim.html')
            
    else:
        user_form = UserRegistrationForm()
    
    return render(request,'AccountApp/register.html',{'user_form':user_form})


def PassGen():
    # create a random password 
    # lenght = 6
    # lower case , uppercase and numbers

    valid_Chars = string.ascii_lowercase
    valid_Chars += string.ascii_uppercase
    valid_Chars += '0123456789'

    GenPass = ''

    for i in range(6):
        GenPass += random.choice(valid_Chars)

    return GenPass

def Confrim_check(request):
    Confrim_Pass = request.POST.get('Confpass')
    MainPass = request.session.get('MainPass')
    
    if Confrim_Pass == MainPass:
        # create user

        global new_user
        global user_form
        new_user.save()
        national_id = user_form.cleaned_data['national_id']
        phone = user_form.cleaned_data['phone']

        Profile.objects.create(user=new_user,phone=phone,national_id=national_id)

        return HttpResponseRedirect(reverse('AccountApp:login'))
    else :
        return render(request,'AccountApp/Confrim.html',{'error':'کد تایید شما نادرست است.'})