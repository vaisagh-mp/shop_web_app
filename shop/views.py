from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Cart, CartItem, Order, Rating, Address
from .forms import ProductForm, AddressForm, RatingForm, CustomerCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import OrderStatusForm


def register_employee(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Log the user in immediately after creation
            login(request, user)

            # Redirect to the customer home page after registration
            return redirect('customer_home')  # Modify this target URL as needed
        else:
            # If the form is invalid, render the registration page with the form and errors
            return render(request, 'customers/register.html', {'form': form})
    else:
        form = CustomerCreationForm()

    # Render the registration page if the request method is GET
    return render(request, 'customers/register.html', {'form': form})

# Custom Login View
def custom_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_home')  # Redirect to admin home
        else:
            return redirect('customer_home')  # Redirect to customer home

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_home')  # Redirect to admin home
                else:
                    return redirect('customer_home')  # Redirect to customer home
            else:
                return HttpResponse('Invalid login credentials', status=401)
        else:
            return HttpResponse('Invalid login form', status=400)
    else:
        form = AuthenticationForm()

    return render(request, 'customers/login.html', {'form': form})

# Custom Logout View
def custom_logout(request):
    logout(request)
    return redirect('custom-login')  # Redirect to login page


# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

# Admin Views
@staff_member_required
def admin_home(request):
    return render(request, 'shop/admin_home.html', {'products': Product.objects.all()})

@staff_member_required
def view_all_products(request):
    products = Product.objects.all()  # Get all products from the database
    return render(request, 'admin/view_all_products.html', {'products': products})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = ProductForm()
    return render(request, 'admin/add_product.html', {'form': form})

@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/edit_product.html', {'form': form})

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_home')

@staff_member_required
def view_orders(request):
    orders = Order.objects.all()
    return render(request, 'admin/view_orders.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('view_orders')  # Redirect to the orders view page
    else:
        form = OrderStatusForm(instance=order)
    
    return render(request, 'admin/update_order_status.html', {'form': form, 'order': order})

# Customer Views
@login_required
def customer_home(request):
    products = Product.objects.all()
    return render(request, 'customers/home.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    # Fetch the cart for the currently logged-in user
    try:
        cart = Cart.objects.get(customer=request.user)  # Access the cart by user
        cart_items = cart.items.all()  # Get all items in the cart
        total = sum(item.product.price * item.quantity for item in cart_items)  # Calculate the total price
    except Cart.DoesNotExist:
        cart_items = []
        total = 0

    return render(request, 'customers/view_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    })

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, customer=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user
            address.save()
            for item in cart.items.all():
                Order.objects.create(customer=request.user, product=item.product, quantity=item.quantity)
            cart.items.all().delete()
            return redirect('view_orders_customer')
    else:
        form = AddressForm()
    return render(request, 'customers/place_order.html', {'form': form})

@login_required
def view_orders_customer(request):
    orders = request.user.orders.all()
    return render(request, 'customers/view_orders.html', {'orders': orders})

@login_required
def view_order_details(request, order_id):
    # Get the order by ID, ensuring it's the current logged-in user's order
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    return render(request, 'customers/order_details.html', {'order': order})

@login_required
def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.customer = request.user
            rating.product = product
            rating.save()
            return redirect('customer_home')
    else:
        form = RatingForm()
    return render(request, 'customers/rate_product.html', {'form': form, 'product': product})
