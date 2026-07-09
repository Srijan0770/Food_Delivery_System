from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('my/', views.my_restaurant, name='my_restaurant'),
    path('create/', views.create_restaurant, name='create_restaurant'),
    path('<int:pk>/edit/', views.edit_restaurant, name='edit_restaurant'),
]
