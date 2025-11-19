from django.shortcuts import redirect,render,get_object_or_404
from. models import Product
from . models import Cartitems

# Create your views here.
def product_list(request):
    uploads=Product.objects.all()
    return render(request,'men.html',{'uploads':uploads})


def product_details(request,product_id):
    upload=get_object_or_404(Product,id=product_id)
    return render(request,'product_details.html',{'upload':upload})



def cart(request):
    cart_items=Cartitems.objects.all()
    total_amount=sum(item.total_price for item in cart_items)
    return render(request,'cart.html',{
        'cart_items':cart_items,
        'total_amount':total_amount
    })



def add_to_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    cart_item,created=Cartitems.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('cart')    


from .models import Cartitems
# Update quantity in cart
def update_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cartitems,id=cart_item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # if set to 0 → remove item
    return redirect('cart')



# Remove item from cart
def remove_from_cart(request,cart_item_id):
    cart_item = get_object_or_404(Cartitems, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

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

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')  # <-- redirect to login page after successful registration

    return render(request, 'register.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')  # re-render login with error

    return render(request, 'login.html')

# Dashboard view (protected)
@login_required(login_url='login')
def dashboard_view(request):
    user = request.user
    return render(request, 'dashboard.html', {'user': user})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
