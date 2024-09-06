from django.shortcuts import render
from .models import Profile,Menu, Product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# def index (request):
#     return render(request, 'index.html', {})

def menuhome(request, resturant_id):
    profile = get_object_or_404(Profile, id=resturant_id)
    
    menus = Menu.objects.filter(user=profile.user)
    products = Product.objects.filter(menu__user=profile.user)
    
    context = {
        'products': products,
        'menus': menus,
        'resturant': profile,
        'active_view': 'all'
    }
    return render(request, 'all.html', context)



def menu(request, resturant_id, menu_id):
    profile = get_object_or_404(Profile, id=resturant_id)
    
    current_menu = get_object_or_404(Menu, user=profile.user, id=menu_id)
    menus = Menu.objects.filter(user=profile.user)
    products = Product.objects.filter(menu=current_menu)
    
    context = {
        'products': products,
        'menus': menus,
        'resturant': profile,
        'menu_id':current_menu.id,
        'active_view': 'menu'
    }
    print(context)
    return render(request, 'menu.html',context )
