from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:resturant_id>/', views.menuhome, name='menuhome'),    
    path('<int:resturant_id>/<int:menu_id>/', views.menuhome, name='menu'),
    path('<int:resturant_id>/product/<int:product_id>/', views.item, name='product'),
    path('<int:resturant_id>/cart/', include('cart.urls')),

]
