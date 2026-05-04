from django.urls import path
from . import views

app_name = 'bags'

urlpatterns = [
    path('', views.bag_list, name='bag_list'),
]