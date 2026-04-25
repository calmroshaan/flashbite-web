from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    # The main browse/search page
    path('', views.store_list, name='store_list'),
    
    # Store Owner Dashboard
    path('owner-dashboard/', views.owner_dashboard, name='owner_dashboard'),

    # Add a new bag
    path('owner-dashboard/add-bag/', views.add_bag, name='add_bag'),
    
    # The individual store detail page
    path('<slug:slug>/', views.store_detail, name='store_detail'),
]