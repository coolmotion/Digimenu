from django.urls import path
from . import views

urlpatterns = [
    path('<int:resturant_id>/', views.menuhome, name='menuhome'),    
    path('<int:resturant_id>/<int:menu_id>/', views.menu, name='menu'),
]
