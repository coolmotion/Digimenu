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
    restaurant_name = profile.resturant_name if profile.resturant_name else "Default Restaurant Name"
    # restaurant_image = profile.image if profile.image else "default_image_url.jpg"  # or use a default image URL
    products = Product.objects.filter(menu__user=profile.user)

    context = {
        'restaurant_name': restaurant_name,
        # 'restaurant_image': profile.image,
        'menus': menus,  
        'products': products,  
    }
    return render(request, 'dashboard.html', context )

@login_required
def dashboard_menu(request, menu_id=None):
    profile = get_object_or_404(Profile, user=request.user)

    menus = Menu.objects.filter(user=profile.user)
    restaurant_name = profile.resturant_name if profile.resturant_name else "Default Restaurant Name"
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
        'restaurant_name': restaurant_name,
        # 'restaurant_image': profile.image,
        'menus': menus,  
        'selected_menu': selected_menu,  
        'products': products,  
    }
    print(menu_id)
    return render(request, 'dashboard.html', context )

def product_info(request, product_id=None):
    if product_id is not None:

        product = get_object_or_404(Product, id=product_id)

        if request.method == 'POST':
            new_name = request.POST.get('name')
            new_description = request.POST.get('description')
            new_price = request.POST.get('price')

            if new_name:
                product.name = new_name

            if new_description:
                product.description = new_description
            
            if new_price:
                product.price = new_price
                print(new_price)

            product.save()
            messages.success(request, "Your product was added.")


        context = {
            'name': product.name,
            'description': product.description,
            'menu': product.menu,
            'price': product.price,
            'image': product.image

        }
        return render(request, 'product_info.html', context)
    
    return HttpResponse("Product ID not provided.")

@login_required
def add_product(request):
    menus = Menu.objects.filter(user=request.user)
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
    return render(request, 'addproduct.html' , {'menus': menus})

@login_required
def add_menu(request):

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
    
    return render(request, 'addmenu.html' , {'menus': menus})  

@login_required
def change_menu(request, menu_id):
    edit_menu = get_object_or_404(Menu, id=menu_id, user=request.user)  
    menus = Menu.objects.filter(user=request.user)


    if request.method == 'POST':
        name = request.POST.get('name')

        if name:  # Basic validation to ensure name is provided
            edit_menu.name = name
            edit_menu.save()
            messages.success(request, "Menu updated successfully!")
            return redirect('dashboard')  # Redirect to a menu list or another page
        else:
            messages.error(request, "Please provide a valid menu name.")
    
    return render(request, 'changemenu.html', {'edit_menu': edit_menu , 'menus': menus})

@login_required
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id, user=request.user) 
    if request.method == 'POST':
        menu.delete()
        messages.success(request, "Menu deleted successfully!")
        return redirect('dashboard')  

    return redirect('dashboard')  