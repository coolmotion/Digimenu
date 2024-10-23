from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
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
    product_list = Product.objects.filter(menu__in=categories).order_by('name')

    paginator = Paginator(product_list, 10)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'menus': categories,
        'products': products, 
        'title': 'Dashboard' 
    }
    return render(request, 'dashboard.html', context)

@login_required
def menu_products(request, menu_id=None):
    profile = get_object_or_404(Profile, user=request.user)
    categories = Category.objects.filter(resturant=profile)
    if categories.exists():
        if menu_id is None:
            first_menu = categories.first()
            menu_id = first_menu.id
        
        selected_menu = get_object_or_404(Category, id=menu_id)
        
        products = Product.objects.filter(menu=selected_menu)
    else:
        selected_menu = None
        products = []

    context = {
        'selected_menu': selected_menu,  
        'products': products,
        'title': 'All products'  
    }
    print(menu_id)
    return render(request, 'dashboard.html', context )

@login_required
def product_info(request, product_id):
    product = get_object_or_404(Product, id=product_id, resturant=request.user.profile)

    if request.method == 'POST':
        if 'submit_product' in request.POST:
            product_form = ProductForm(request.POST, request.FILES, instance=product, user_profile=request.user.profile)
            if product_form.is_valid():
                product_form.save()
                print('Product saved')
                return redirect('dashboard')
        elif 'submit_portion' in request.POST:
            portion_formset = PortionFormSetNoExtra(request.POST, request.FILES, instance=product)
            if portion_formset.is_valid():
                portion_formset.save()
                print('Portion saved')
                return redirect('dashboard')
    else:
        product_form = ProductForm(instance=product, user_profile=request.user.profile)
        portion_formset = PortionFormSet(instance=product)

    context =  {
        'product_form': product_form,
        'portion_formset': portion_formset,
        'product': product,
        'title': 'Product info' 
    }
    return render(request, 'product_info.html', context)
    
@login_required
def add_product(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        product_form = ProductForm(user_profile=profile, data=request.POST, files=request.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.resturant = profile  
            new_product.save()
            return redirect('dashboard') 
    else:
        product_form = ProductForm(user_profile=profile)
    
    context = {
        'product_form': product_form,
        'title': 'Add product' 
    }
    return render(request, 'add_product.html', context)

@login_required
def add_menu(request):
    profile = get_object_or_404(Profile, user=request.user)
    categories = Category.objects.filter(resturant=profile)
    if request.method == 'POST':
        name = request.POST.get('name') 
        if name:  
            new_menu = Category(resturant=profile,  name=name)
            new_menu.save()
            messages.success(request, "New menu created successfully!")
            return redirect('dashboard')  
        else:
            messages.error(request, "Please provide a valid menu name.")
    context = {
        'menus': categories ,
        'title': 'Add menu' 
        }
    return render(request, 'addmenu.html', context)  

@login_required
def change_menu(request, menu_id):
    edit_menu = get_object_or_404(Category, id=menu_id, user=request.user)  
    menus = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')

        if name: 
            edit_menu.name = name
            edit_menu.save()
            messages.success(request, "Menu updated successfully!")
            return redirect('dashboard')  
        else:
            messages.error(request, "Please provide a valid menu name.")
    
    context = {
        'edit_menu': edit_menu , 
        'menus': menus, 
        'title': 'Change menu' 
        }
    return render(request, 'changemenu.html', context )

@login_required
def delete_menu(request, menu_id):
    menu = get_object_or_404(Category, id=menu_id) 
    if request.method == 'POST':
        menu.delete()
        messages.success(request, "Menu deleted successfully!")
        return redirect('dashboard')  

    return redirect('dashboard')  

def generate_qr_code(request, resturant_id):
    profile = get_object_or_404(Profile, user=request.user)
    id = profile.id
    url = f"https://digimenu.lk/app/{id}"
    print(url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    
    # Set the filename for the QR code image
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="my_qr_code.png"'
    return response


@login_required
def list_orders(request):

    profile = get_object_or_404(Profile, user=request.user)

    today = now().date()
    orders_list = Order.objects.filter(resturant=profile, date_ordered__date=today).order_by('-date_ordered')

    paginator = Paginator(orders_list, 10)  
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'orders': orders,
        'title': 'Orders'  
    }
    return render(request, 'orders.html', context)


def add_menu(request):
    profile = get_object_or_404(Profile, user=request.user)
    categories = Category.objects.filter(resturant=profile)
    if request.method == 'POST':
        name = request.POST.get('name') 
        if name:  
            new_menu = Category(resturant=profile,  name=name)
            new_menu.save()
            messages.success(request, "New menu created successfully!")
            return redirect('dashboard')  
        else:
            messages.error(request, "Please provide a valid menu name.")
    context = {
        'menus': categories ,
        'profile': profile,
        'title' : 'Add menu',
        }
    return render(request, 'addmenu.html' , context)  