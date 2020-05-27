from django.urls import path
from . import views

# app_name = "blog"

urlpatterns = [
    path('hotel/<id>/reserve', views.hotel_pre_reserve, name='hotel_pre_reserve')
]