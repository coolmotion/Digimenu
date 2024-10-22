from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Profile,Category, Product
from cart.models import Order
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import ProductForm, PortionFormSet, PortionFormSetNoExtra
import qrcode
from django.core.paginator import Paginator
from io import BytesIO
from django.utils.timezone import now

@login_required
def dashboard(request, menu_id=None):
    profile = get_object_or_404(Profile, user=request.user)
    categories = Category.objects.filter(resturant=profile)
    products = Product.objects.filter(menu__in=categories)

    context = {
        'profile': profile,
        'menus': categories,
        'products': products,  
    }
    return render(request, 'dashboard.html', context)

@login_required
def dashboard_menu(request, menu_id=None):
    profile = get_object_or_404(Profile, user=request.user)

    menus = Category.objects.filter(user=profile.user)
    # restaurant_image = profile.image if profile.image else "default_image_url.jpg"  # or use a default image URL

    if menus.exists():
        if menu_id is None:
            first_menu = menus.first()
            menu_id = first_menu.id
        
        selected_menu = get_object_or_404(Category, id=menu_id, user=profile.user)
        
        products = Product.objects.filter(menu=selected_menu)
    else:
        selected_menu = None
        products = []

    context = {
        'profile': profile,
        'menus': menus,  
        'selected_menu': selected_menu,  
        'products': products,  
    }
    print(menu_id)
    return render(request, 'dashboard.html', context )


# def product_info(request, product_id):
#     product = get_object_or_404(Product, id=product_id, resturant=request.user.profile)
    
#     if request.method == 'POST':
#         if 'product_form' in request.POST:
#             product_form = ProductForm(request.POST, request.FILES, instance=product, user_profile=request.user.profile)
#             if product_form.is_valid():
#                 product_form.save()
#                 messages.success(request, "Product details updated successfully.")
#                 return redirect('product_info', product_id=product.id)
#         elif 'portion_formset' in request.POST:
#             portion_formset = PortionFormSetNoExtra(request.POST, instance=product)
#             if portion_formset.is_valid():
#                 portion_formset.save()
#                 messages.success(request, "Portions updated successfully.")
#                 return redirect('product_info', product_id=product.id)

#     else:
#         product_form = ProductForm(instance=product, user_profile=request.user.profile)
#         portion_formset = PortionFormSetNoExtra(instance=product)

#     return render(request, 'product_info.html', {
#         'product_form': product_form,
#         'portion_formset': portion_formset,
#         'product': product
#     })
@login_required
def product_info(request, product_id):
    product = get_object_or_404(Product, id=product_id, resturant=request.user.profile)
    
    if request.method == 'POST':
        if 'submit_product' in request.POST:
            product_form = ProductForm(request.POST, request.FILES, instance=product, user_profile=request.user.profile)
            if product_form.is_valid():
                product_form.save()
                print('Product saved')
                return redirect('dashboard')  # Redirect to avoid repost on refresh
        elif 'submit_portion' in request.POST:
            portion_formset = PortionFormSetNoExtra(request.POST, request.FILES, instance=product)
            if portion_formset.is_valid():
                portion_formset.save()
                print('Portion saved')
                return redirect('dashboard')  # Redirect to avoid repost on refresh
    else:
        product_form = ProductForm(instance=product, user_profile=request.user.profile)
        portion_formset = PortionFormSetNoExtra(instance=product)

    return render(request, 'product_info.html', {
        'product_form': product_form,
        'portion_formset': portion_formset,
        'product': product
    })
    
@login_required
def add_product(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        print(request.POST)
        product_form = ProductForm(request.POST, request.FILES, user_profile=user_profile)
        portion_formset = PortionFormSet(request.POST)
        
        if product_form.is_valid() and portion_formset.is_valid():
            product = product_form.save(commit=False)
            product.resturant = user_profile
            product.save()
            print("Product saved:", product)

            portions = portion_formset.save(commit=False)
            for portion in portions:
                portion.product = product
                portion.save()
                print("Portion saved:", portion)

        return redirect('dashboard')  # Redirect to the dashboard
            
    else:
        product_form = ProductForm(user_profile=user_profile)
        portion_formset = PortionFormSet()
    
    return render(request, 'add_product.html', {
        'product_form': product_form,
        'portion_formset': portion_formset,
    })

@login_required
def change_menu(request, menu_id):
    edit_menu = get_object_or_404(Category, id=menu_id, user=request.user)  
    menus = Category.objects.filter(user=request.user)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')

        if name:  # Basic validation to ensure name is provided
            edit_menu.name = name
            edit_menu.save()
            messages.success(request, "Menu updated successfully!")
            return redirect('dashboard')  # Redirect to a menu list or another page
        else:
            messages.error(request, "Please provide a valid menu name.")
    
    return render(request, 'changemenu.html', {'edit_menu': edit_menu , 'menus': menus, 'profile':profile})

@login_required
def delete_menu(request, menu_id):
    menu = get_object_or_404(Category, id=menu_id, user=request.user) 
    if request.method == 'POST':
        menu.delete()
        messages.success(request, "Menu deleted successfully!")
        return redirect('dashboard')  

    return redirect('dashboard')  

def generate_qr_code(request, resturant_id):
    # Create the URL for the restaurant's menu page using the resturant_id
    # profile = get_object_or_404(Profile, user=request.user)
    # resturant_id = profile.id
    menu_url = request.build_absolute_uri(reverse('menuhome', args=[resturant_id]))

    # Create a QR code that redirects to the menu URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a bytes buffer
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the image as an HTTP response with the proper content type
    return HttpResponse(buffer, content_type='image/png')

@login_required
def list_orders(request):
    # Assuming 'user' is linked to 'Profile' and 'Profile' has a one-to-one relationship with 'User'
    restaurant = request.user.profile
    profile = get_object_or_404(Profile, user=request.user)

    categories = Category.objects.filter(resturant=profile)
    products = Product.objects.filter(menu__in=categories)

    # Filter orders by the current date
    today = now().date()
    orders_list = Order.objects.filter(resturant=restaurant, date_ordered__date=today).order_by('-date_ordered')

    # Paginate the orders - 10 orders per page
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'restaurant': restaurant,
        'orders': orders,
        'profile': profile,
        'menus': categories,  
    }
    return render(request, 'orders.html', context)

@login_required
def add_menu(request):
    profile = get_object_or_404(Profile, user=request.user)
    menus = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name') 
        if name:  
            new_menu = Category(
                user=request.user,  
                name=name
            )
            new_menu.save()
            messages.success(request, "New menu created successfully!")
            return redirect('dashboard')  
        else:
            messages.error(request, "Please provide a valid menu name.")
    
    return render(request, 'addmenu.html' , {'menus': menus ,'profile': profile})  