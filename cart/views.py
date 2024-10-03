from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from main.models import Product, Portion, Profile
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
import json

def cart_add(request, resturant_id):
    cart = Cart(request, app_id=resturant_id)
    if request.POST.get('action') == 'post':
        portion_id = int(request.POST.get('product_id'))
        portion_qty = int(request.POST.get('product_qty'))
        portion = get_object_or_404(Portion, id=portion_id)
        cart.add(portion=portion, quantity=portion_qty, app_id=resturant_id)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("product Added To Cart..."))
        return response

      
def cart_summary(request, resturant_id):
    
    cart = Cart(request, app_id=resturant_id)
    cart_portions = cart.get_prods	
    quantities = cart.get_quants 	
    totals = cart.cart_total(app_id=resturant_id)
    total_items = cart.__len__	

    context = {
        'cart_portions':cart_portions,
        'quantities':quantities,
        'total_items': total_items,
        'totals':totals
    }

    return render(request, 'summary.html', context)

def cart_update(request, resturant_id):
    cart = Cart(request, app_id=resturant_id)
    if request.POST.get('action') == 'post':
        portion_id = int(request.POST.get('product_id'))
        portion_qty = int(request.POST.get('product_qty'))

        cart.update(portion=portion_id, quantity=portion_qty ,app_id=resturant_id)

        response = JsonResponse({'qty': portion_qty})
        print(portion_qty)
        messages.success(request, "Your Cart Has Been Updated...")
        return response

def cart_delete(request, resturant_id):
    cart = Cart(request, app_id=resturant_id)
    if request.POST.get('action') == 'post':
        portion_id = int(request.POST.get('product_id'))
        cart.delete(portion=portion_id, app_id=resturant_id)

        return redirect('summary',  resturant_id=resturant_id)
      
@require_POST
def process_order(request, resturant_id):
    phone_number = request.POST.get('phone')
    cart = Cart(request, app_id=resturant_id)
    quantities = cart.get_quants
    amount_paid = cart.cart_total()
    cart_portions = cart.get_prods

    create_order = Order(phone=phone_number, amount_paid=amount_paid)
    try:
        create_order.save()
        print(f"Order saved successfully for phone number: {phone_number}")
        order_id = create_order.pk
        for portion in cart_portions():
            portion_id = portion.id
            price = portion.price

            for key, value in quantities().items():
                if int(key) == portion_id:
                    # Create order item
                    create_order_item = OrderItem(order_id=order_id, portion_id=portion_id, quantity=value, price=price)
                    create_order_item.save()

        # Clear relevant session keys
        for key in list(request.session.keys()):
            if key == "session_key":
                # Delete the key
                del request.session[key]
        messages.success(request, "Order Placed!")

    except Exception as e:
        print(f"Failed to save order for phone number: {phone_number}. Error: {e}")

    # Redirect the user to a new page or back to the form with a success message
    return redirect('home')
