from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:resturant_id>/', views.menuhome, name='menuhome'),    
    path('<int:resturant_id>/<int:category_id>/', views.menuhome, name='menu'),
    path('<int:resturant_id>/product/<int:product_id>/', views.product, name='product'),
    path('<int:resturant_id>/cart/', include('cart.urls')),

]
