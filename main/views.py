from django.shortcuts import render
from .models import Profile, Category, Product, Portion
from django.http import HttpResponse
from cart.cart import Cart
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


def menuhome(request, resturant_id, category_id=None):
    profile = get_object_or_404(Profile, id=resturant_id)
    
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products_qs = Product.objects.filter(menu=current_category)
        active_view = 'menu'
    else:
        categories = Category.objects.filter(resturant=profile)
        products_qs = Product.objects.filter(menu__in=categories).order_by('?')
        active_view = 'all'

    paginator = Paginator(products_qs, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    product_ids = products.object_list.values_list('id', flat=True)
    portions = Portion.objects.filter(product_id__in=product_ids)

    nums = "a" * paginator.num_pages

    context = {
        'portions': portions,
        'active_view': active_view,
        'products': products,
        'nums': nums,
        'menu_id': category_id if category_id else None,
    }

    return render(request, 'all.html', context)

def product(request,resturant_id, product_id):

    profile = get_object_or_404(Profile, id=resturant_id)
    categories = Category.objects.filter(resturant=profile)
    product = get_object_or_404(Product, id=product_id)
    current_menu = product.menu

    context = {
        'product': product,
        'menus': categories,
        'resturant': profile,
        'menu_id':current_menu.id,
        'active_view': 'menu'
    }
    return render(request, 'product.html', context)