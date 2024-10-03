from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Profile,Menu, Product
from cart.models import Order
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import ProductForm
import qrcode
from io import BytesIO

@login_required
def dashboard(request, menu_id=None):
    profile = get_object_or_404(Profile, user=request.user)

    menus = Menu.objects.filter(user=profile.user)
    # restaurant_image = profile.image if profile.image else "default_image_url.jpg"  # or use a default image URL
    products = Product.objects.filter(menu__user=profile.user)

    context = {
        'profile': profile,
        # 'restaurant_image': profile.image,
        'menus': menus,  
        'products': products,  
    }
    return render(request, 'dashboard.html', context )

@login_required
def dashboard_menu(request, menu_id=None):
    profile = get_object_or_404(Profile, user=request.user)

    menus = Menu.objects.filter(user=profile.user)
    # restaurant_image = profile.image if profile.image else "default_image_url.jpg"  # or use a default image URL

    if menus.exists():
        if menu_id is None:
            first_menu = menus.first()
            menu_id = first_menu.id
        
        selected_menu = get_object_or_404(Menu, id=menu_id, user=profile.user)
        
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

@login_required
def product_info(request, product_id):
    profile = get_object_or_404(Profile, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Your product was updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    context = {
        'profile': profile,
        'name': product.name,
        'description': product.description,
        'menu': product.menu,
        'price': '500',
        'image': product.image
    }

    return render(request, 'product_info.html', context)
    


@login_required
def add_product(request):
    menus = Menu.objects.filter(user=request.user)
    profile = get_object_or_404(Profile, user=request.user)

    if not menus.exists():
        messages.error(request, "You need to create a menu before adding products.")

        return redirect('add_menu')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        menu = request.POST.get('menu')
        image = request.FILES.get('image')  # If you want to handle image uploads

        if name and price and menu and description and image:  # Basic validation to check required fields
            new_product = Product(
                name=name,
                description=description,
                price=price,
                menu_id=menu,  # Assuming menu is a ForeignKey
                image=image  # Optional image field
            )
            new_product.save()
            messages.success(request, "New product created successfully!")
            return redirect('product_info', product_id=new_product.id)
        else:
            messages.error(request, "Please fill in all required fields.")
    # messages.error(request, "This page is under construction.")
    return render(request, 'addproduct.html' , {'menus': menus, 'profile': profile,})

@login_required
def add_menu(request):
    profile = get_object_or_404(Profile, user=request.user)
    menus = Menu.objects.filter(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name') 
        if name:  
            new_menu = Menu(
                user=request.user,  
                name=name
            )
            new_menu.save()
            messages.success(request, "New menu created successfully!")
            return redirect('dashboard')  
        else:
            messages.error(request, "Please provide a valid menu name.")
    
    return render(request, 'addmenu.html' , {'menus': menus ,'profile': profile})  

@login_required
def change_menu(request, menu_id):
    edit_menu = get_object_or_404(Menu, id=menu_id, user=request.user)  
    menus = Menu.objects.filter(user=request.user)
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
    menu = get_object_or_404(Menu, id=menu_id, user=request.user) 
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

    menus = Menu.objects.filter(user=profile.user)
    # restaurant_image = profile.image if profile.image else "default_image_url.jpg"  # or use a default image URL
    products = Product.objects.filter(menu__user=profile.user)
    orders = Order.objects.filter(resturant=restaurant).order_by('-date_ordered')
    context = {
        'restaurant': restaurant,
        'orders': orders,
        'profile': profile,
        # 'restaurant_image': profile.image,
        'menus': menus,  
    }
    return render(request, 'orders.html', context)

