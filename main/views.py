from django.shortcuts import render
from .models import Profile,Menu, Product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# def index (request):
#     return render(request, 'index.html', {})

def hello_restaurant(request, resturant_name):
    # Retrieve the profile associated with the restaurant name
    profile = get_object_or_404(Profile, resturant_name=resturant_name)
    
    # Retrieve all menus associated with the profile's user
    menus = Menu.objects.filter(user=profile.user)
    
    # Prepare context data to pass to the template
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
                'description': product.description,
                'is_sale': product.is_sale,
                'sale_price': product.sale_price,
                'image': product.image.url if product.image else None
            }
            menu_info['products'].append(product_info)
        
        context['menus'].append(menu_info)
    
    return render(request, 'products.html', context)

def menu(request, resturant_name, menu_name):
    # Retrieve the profile associated with the restaurant name
    profile = get_object_or_404(Profile, resturant_name=resturant_name)
    
    # Retrieve all menus associated with the profile's user
    menu = get_object_or_404(Menu, user=profile.user, name=menu_name)
    menus = Menu.objects.filter(user=profile.user)
    products = Product.objects.filter(menu=menu)

    
    
    return render(request, 'menu.html',  {'products': products, 'menus': menus, 'resturant':profile })

