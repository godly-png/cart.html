from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from decimal import Decimal

from .models import Product, Cartitems, BillingDetails, Order, OrderItem
from .forms import BillingDetailsForm


# -------------------------------
# PRODUCT LIST & DETAILS
# -------------------------------
def product_list(request):
    uploads = Product.objects.all()
    return render(request, 'men.html', {'uploads': uploads})


def product_details(request, product_id):
    upload = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'upload': upload})


# -------------------------------
# CART
# -------------------------------
def cart(request):
    cart_items = Cartitems.objects.all()
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })


from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cartitems
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the cart item exists for THIS user and product
    cart_item, created = Cartitems.objects.get_or_create(
        product=product,
        user=request.user  # <-- associate with logged-in user
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def update_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cartitems, id=cart_item_id, user=request.user)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cartitems, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


# -------------------------------
# AUTH
# -------------------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard_view(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard.html', {
        'user': request.user,
        'orders': user_orders
    })


def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard.html')  # create dashboard.html template




# -------------------------------
# CHECKOUT - CORRECTED VERSION
# -------------------------------
from django.shortcuts import render, redirect
from .models import BillingDetails, Order, OrderItem
from .forms import BillingDetailsForm
from .models import Cartitems
@login_required
def checkout(request):
    cart_items = Cartitems.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        form = BillingDetailsForm(request.POST)
        if form.is_valid():

            # Save billing details
            billing = form.save(commit=False)
            billing.user = request.user
            billing.save()

            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                billing_details=billing  # <-- CORRECT FIELD
            )

            # Save all order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price * item.quantity
                )

            # Empty cart
            cart_items.delete()

            return redirect("checkout_success", order_id=order.id)

    else:
            form =BillingDetailsForm()

    return render(request, "checkout.html", {
        "form": form,
        "cart": cart_items,
        "total": total_amount
    })



def billing_page(request):
    return render(request, 'billing.html')


@login_required
def summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    return render(request, "summary.html", {
        "order": order,
        "items": items
    })


def place_order(request):
    if request.method == "POST":
        form = BillingDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = BillingDetailsForm()

    return render(request, 'checkout.html', {'form': form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    return render(request, 'order_detail.html', {
        'order': order,
        'items': items
    })







import razorpay
from django.conf import settings

def order_success(request):
    latest_order = Order.objects.order_by('-id').first()

    if not latest_order:
        messages.error(request, "No order found!")
        return redirect('cart')

    # Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Amount must be in PAISA
    razorpay_order = client.order.create({
        "amount": int(latest_order.total * 100),   # convert to paisa
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "order": latest_order,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": latest_order.total * 100,  # in paisa for JS
    }

    return render(request, "order_success.html", context)

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db import transaction
# from decimal import Decimal
# from django.conf import settings


# from .models import Product, Cartitems, BillingDetails, Order, OrderItem
# from .forms import BillingDetailsForm
# import razorpay

# # --------- PRODUCT VIEWS ---------
# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'men.html', {'uploads': products})

# def product_details(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'product_details.html', {'upload': product})

# # --------- CART VIEWS ---------
# @login_required
# def cart(request):
#     cart_items = Cartitems.objects.filter(user=request.user)
#     total_amount = sum(item.total_price for item in cart_items)
#     return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart_item, created = Cartitems.objects.get_or_create(user=request.user, product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('cart')

# @login_required
# def remove_from_cart(request, cart_item_id):
#     cart_item = get_object_or_404(Cartitems, id=cart_item_id, user=request.user)
#     cart_item.delete()
#     return redirect('cart')

# @login_required
# def update_from_cart(request, cart_item_id):
#     cart_item = get_object_or_404(Cartitems, id=cart_item_id, user=request.user)
#     if request.method == 'POST':
#         qty = int(request.POST.get('quantity', 1))
#         if qty > 0:
#             cart_item.quantity = qty
#             cart_item.save()
#         else:
#             cart_item.delete()
#     return redirect('cart')

# # --------- CHECKOUT & BILLING ---------
# @login_required
# def checkout(request):
#     cart_items = Cartitems.objects.filter(user=request.user)
#     if not cart_items.exists():
#         messages.warning(request, "Your cart is empty!")
#         return redirect('cart')

#     total_amount = sum(item.total_price for item in cart_items)

#     if request.method == "POST":
#         form = BillingDetailsForm(request.POST)
#         if form.is_valid():
#             billing = form.save(commit=False)
#             billing.user = request.user
#             billing.save()

#             order = Order.objects.create(
#                 user=request.user,
#                 total_amount=total_amount,
#                 billing_details=billing
#             )

#             for item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product_name=item.product.name,
#                     quantity=item.quantity,
#                     price=item.total_price
#                 )

#             cart_items.delete()
#             return redirect('checkout_success', order_id=order.id)
#     else:
#         form = BillingDetailsForm()

#     return render(request, 'checkout.html', {'form': form, 'cart': cart_items, 'total': total_amount})

# # --------- ORDER SUMMARY & PAYMENT ---------
# @login_required
# def checkout_success(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     items = order.items.all()

#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     razorpay_order = client.order.create({
#         "amount": int(order.total_amount * 100),
#         "currency": "INR",
#         "payment_capture": "1"
#     })

#     return render(request, "summary.html", {
#         "order": order,
#         "items": items,
#         "razorpay_order_id": razorpay_order['id'],
#         "razorpay_key": settings.RAZORPAY_KEY_ID,
#         "amount": int(order.total_amount * 100)
#     })

@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()

    # Calculate amount in paisa
    amount_in_paisa = int(order.total_amount * 100)

    # Ensure minimum Razorpay amount (₹1 = 100 paisa)
    if amount_in_paisa < 100:
        messages.error(request, "Order amount must be at least ₹1 for payment.")
        return redirect('cart')

    # Razorpay Client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({
        "amount": amount_in_paisa,
        "currency": "INR",
        "payment_capture": 1  # integer 1, not string
    })

    return render(request, "summary.html", {
        "order": order,
        "items": items,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount_in_paisa
    })
