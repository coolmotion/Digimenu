from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Profile,Menu, Product
from django.shortcuts import get_object_or_404


@login_required
def dashboard(request, menu_id=None):
    profile = get_object_or_404(Profile, user=request.user)

    menus = Menu.objects.filter(user=profile.user)
    context = {
        'restaurant_name': profile.resturant_name,
        'restaurant_image': profile.image,
        'menus': []
    }
    if menu_id is None:
        first_menu = menus.first()
        menu_id = first_menu.id
    
    selected_menu = get_object_or_404(Menu, id=menu_id, user=profile.user)
    
    products = Product.objects.filter(menu=selected_menu)

    context = {
        'restaurant_name': profile.resturant_name,
        'restaurant_image': profile.image,
        'menus': menus,  
        'selected_menu': selected_menu,  
        'products': products,  
    }
    print(menu_id)
    return render(request, 'dashboard.html', context )

def product_info(request, product_id=None):
    if product_id is not None:

        product = get_object_or_404(Product, id=product_id)

        context = {
            'name': product.name,
            'description': product.description,
            'menu': product.menu,
            'price': product.price,
            'image': product.image

        }
        return render(request, 'product_info.html', context)

    return HttpResponse("Product ID not provided.")