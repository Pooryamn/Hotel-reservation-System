from django.urls import path
from . import views

# app_name = "blog"

urlpatterns = [
    path('hotel/<id>/reserve', views.hotel_reserve, name='hotel_reserve'),
    path('hotel/reserve/<tracking_code>', views.reserve_factor, name='reserve_factor'),
]
