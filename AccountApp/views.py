import random
import string
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from .forms import LoginForm, UserRegistrationForm, ChangeProfileInfoForm, ChangePasswordForm
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

                    return HttpResponseRedirect(reverse('blog:home'))
                
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


@login_required
def profile(request):
    
    flag = 0
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        ### if request came from form1
        if request.POST['form_select'] == 'form1':
            flag = 1
            ### send original username and email for validation in form
            info_form = ChangeProfileInfoForm(request.POST,
                                              username=user.username,
                                              email=user.email)
            if info_form.is_valid():

                user.username = info_form.cleaned_data['username']
                user.first_name = info_form.cleaned_data['first_name']
                user.last_name = info_form.cleaned_data['last_name']
                user.email = info_form.cleaned_data['email']
                profile.national_id = info_form.cleaned_data['national_id']
                profile.phone = info_form.cleaned_data['phone']

                user.save()
                profile.save()

        ### if request came from form2
        elif request.POST['form_select'] == 'form2':
            flag = 2
            pass_form = ChangePasswordForm(request.POST)
            if pass_form.is_valid():
                password = pass_form.cleaned_data["password"]
                user.set_password(password)
                user.save()

    if flag == 0 or flag == 2:
        profile_initial = {'username': user.username,
                           'first_name':user.first_name,
                           'last_name':user.last_name,
                           'email':user.email,
                           'national_id':profile.national_id,
                           'phone':profile.phone}
        info_form = ChangeProfileInfoForm(initial=profile_initial)
    
    if flag == 0 or flag == 1:
        pass_form = ChangePasswordForm()

    return render(request, 'AccountApp/profile.html', {
            'profile': profile,
            'info_form': info_form,
            'pass_form': pass_form,
        })