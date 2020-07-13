from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    # post views
    url(r'^login/$',views.user_login,name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^confrim/$',views.Confrim_check,name='Confrim_check'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^logout/$', logout, name='logout'),
]