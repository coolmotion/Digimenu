from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('menu/<int:menu_id>/', views.dashboard, name='dashboard_menu'),
    path('product/<int:product_id>/', views.product_info, name='product_info'),
]
