from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/<int:restaurant_pk>/', views.manage_menu, name='manage_menu'),
    path('restaurant/<int:restaurant_pk>/add/', views.add_menu_item, name='add_menu_item'),
    path('<int:pk>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('<int:pk>/delete/', views.delete_menu_item, name='delete_menu_item'),
]
