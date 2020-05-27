from django.urls import path
from . import views

# app_name = "blog"

urlpatterns = [
    path('hotel/<id>/', views.hotel_detail, name='hotel_detail')
]