from django.shortcuts import render
from .models import Profile,Menu, Product, Portion
from django.http import HttpResponse
from cart.cart import Cart
from django.shortcuts import get_object_or_404


def menuhome(request, resturant_id, menu_id=None):
    profile = get_object_or_404(Profile, id=resturant_id)
    
    if menu_id:
        current_menu = get_object_or_404(Menu, user=profile.user, id=menu_id)
        products = Product.objects.filter(menu=current_menu)
        active_view = 'menu'
    else:
        products = Product.objects.filter(menu__user=profile.user)
        active_view = 'all'

    product_ids = products.values_list('id', flat=True)
    portions = Portion.objects.filter(product_id__in=product_ids)

    context = {
        'products': products,
        'portions': portions,
        'active_view': active_view,
    }
    
    if menu_id:
        context['menu_id'] = current_menu.id

    return render(request, 'all.html', context)

def item(request,resturant_id, product_id):

    profile = get_object_or_404(Profile, id=resturant_id)
    menus = Menu.objects.filter(user=profile.user)
    product = get_object_or_404(Product, id=product_id)
    current_menu = product.menu

    context = {
        'product': product,
        'menus': menus,
        'resturant': profile,
        'menu_id':current_menu.id,
        'active_view': 'menu'
    }
    return render(request, 'product.html', context)