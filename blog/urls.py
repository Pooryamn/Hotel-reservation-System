from django.urls import path
from . import views

# app_name = "blog"

urlpatterns = [
    path('hotel/<int:id>', views.hotel_detail, name='hotel_detail'),
    path('hotel/<int:id>/reserve', views.hotel_reserve, name='hotel_reserve'),
    path('hotel/search', views.search, name="search"),
    path('hotel/reserve-factor/<str:tracking_code>', views.reserve_factor, name='reserve_factor'),
]
