from django.urls import path
from . import views

# app_name = "blog"

urlpatterns = [
    path('', views.home_page, name='home'),
    path('<int:id>/', views.hotel_detail, name='hotel_detail'),
    path('<int:id>/reserve/', views.hotel_reserve, name='hotel_reserve'),
    path('search/', views.search, name="search"),
    path('reserve-factor/<str:tracking_code>/', views.reserve_factor, name='reserve_factor'),
    path('reservation-history/', views.reservation_history, name='reservation_history'),
]
