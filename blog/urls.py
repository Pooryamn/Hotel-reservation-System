from django.urls import path
from . import views, api_view

# app_name = "blog"

urlpatterns = [
    path('', views.home_page, name='home'),
    path('hotel/<int:id>/', views.hotel_detail, name='hotel_detail'),
    path('hotel/<int:id>/reserve/', views.hotel_reserve, name='hotel_reserve'),
    path('hotel/search/', views.search, name="search"),
    path('hotel/reserve-factor/<str:tracking_code>/', views.reserve_factor, name='reserve_factor'),
    path('hotel/reservation-history/', views.reservation_history, name='reservation_history'),
    path('hotel/reservation-tracking/', views.reservation_tracking, name='reservation_tracking'),
    path('hotel/compare-hotel/', views.compare_hotel, name='compare_hotel'),
    path('hotel/api/reservation-tracking/',
        api_view.ReserveTrackingAPIView.as_view(),
        name='api_reservation_tracking')
]
