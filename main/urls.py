from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('<str:resturant_name>/', views.hello_restaurant, name='hello_resturant'),    
    path('<str:resturant_name>/<str:menu_name>/', views.menu, name='menu'),
]
