from django.conf.urls import url
from . import views

urlpatterns = [
    # post views
    url('login/',views.user_login,name='login'),
    url('register/',views.register,name='register'),
    url('confrim/',views.Confrim_check,name='Confrim_check'),
]