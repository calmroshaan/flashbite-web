from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('reserve/<int:bag_id>/', views.reserve_bag, name='reserve'),
    path('ticket/<int:pk>/', views.reservation_ticket, name='ticket'),
    path('confirm-pickup/<int:pk>/', views.confirm_pickup, name='confirm_pickup'),
]