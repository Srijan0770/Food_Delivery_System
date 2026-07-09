from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('my/', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
    path('manage/', views.restaurant_orders, name='restaurant_orders'),
    path('<int:pk>/update-status/', views.update_order_status, name='update_order_status'),
]
