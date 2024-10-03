from .cart import Cart


def cart_items(request):
    app_id = request.resolver_match.kwargs.get('resturant_id')
    cart = Cart(request, app_id)  
    return {
        'cart_products': cart.get_prods(),
        'quantities': cart.get_quants(),
        'total_items': cart.__len__(),
        'totals': cart.cart_total(app_id),
    }