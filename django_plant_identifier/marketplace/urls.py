# marketplace/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_home, name='market_home'),
    path('add/', views.add_plant, name='add_plant'),
    path('buy/<int:plant_id>/', views.buy_plant, name='buy_plant'),
    path('purchase/<int:purchase_id>/confirmation/', views.purchase_confirmation, name='purchase_confirmation'),
    path('my-purchases/', views.my_purchases, name='my_purchases'),
    path('my-listings/', views.my_listings, name='my_listings'),
]
