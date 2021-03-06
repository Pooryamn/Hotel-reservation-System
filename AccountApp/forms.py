from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):

    #phone Number:
    phone = forms.CharField(max_length=11, label='Phone number')

    #national ID:
    national_id = forms.CharField(label="National id")
    
    # password 
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    # confrim password
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User

        fields = ('first_name','last_name','email','username')

    def clean_password2(self):
        cd = self.cleaned_data

        if (cd['password'] != cd['password2']):
            raise forms.ValidationError('Passwords do not match !')
            
        return cd['password2']


class ChangeProfileInfoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.req_user = kwargs.pop('username', None)
        self.req_email = kwargs.pop('email', None)
        super(ChangeProfileInfoForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='نام کاربری', required=True)
    
    first_name = forms.CharField(label='نام')

    last_name = forms.CharField(label='نام خانوادگی')

    email = forms.EmailField(label='ایمیل', required=True)

    phone = forms.CharField(label='تلفن همراه', required=False)

    national_id = forms.CharField(label="کد ملی", required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.req_user != username:
            if User.objects.filter(username=username).count():
                raise forms.ValidationError('این نام کاربری در دسترس نمی باشد.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.req_email != email:
            if email and User.objects.filter(email=email).count():
                raise forms.ValidationError('این ایمیل توسط حساب کاربری دیگری در حال استفاده است.')

        return email


class ChangePasswordForm(forms.Form):
    # password 
    password = forms.CharField(label='رمز عبور',widget=forms.PasswordInput)

    # confrim password
    password2 = forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput)

    def clean_password2(self):
            cd = self.cleaned_data

            if (cd['password'] != cd['password2']):
                raise forms.ValidationError('رمز ها همخوانی ندارند.')
                
            return cd['password2']
