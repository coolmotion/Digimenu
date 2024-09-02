from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Profile,Menu, Product
from django.shortcuts import get_object_or_404


@login_required
def dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    menus = Menu.objects.filter(user=profile.user)
    context = {
        'restaurant_name': profile.resturant_name,
        'menus': []
    }
    for menu in menus:
        menu_info = {
            'name': menu.name,
            'products': []
        }
        
        # Retrieve all products associated with this menu
        products = Product.objects.filter(menu=menu)
        
        for product in products:
            product_info = {
                'name': product.name,
                'price': product.price,
                'image': product.image.url if product.image else None
            }
            menu_info['products'].append(product_info)
        
        context['menus'].append(menu_info)
    return render(request, 'dashboard.html', context )