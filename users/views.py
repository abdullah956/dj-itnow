from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from .forms import UserRegistrationForm
from django.contrib.auth import login , logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Category , Product , Cart , Order , ContactMessage
from decimal import Decimal
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'index.html', {'categories': categories,'featured_products': featured_products})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return redirect('cart_view')
    

@login_required(login_url='/login/')
def cart_view(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    
    total_price = Decimal('0.00')
    shipping_cost = Decimal('5.00')

    items_with_totals = []
    
    for item in user_cart_items:
        item_total = item.product.price * Decimal(item.quantity)
        total_price += item_total
        items_with_totals.append({
            'item': item,
            'item_total': item_total
        })
    
    grand_total = total_price + shipping_cost
    
    context = {
        'items_with_totals': items_with_totals,
        'subtotal': total_price,
        'shipping': shipping_cost,
        'total': grand_total,
    }
    return render(request, 'cart.html', context)



def checkout_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        payment_method = request.POST.get('payment_method')
        if payment_method == 'card':
            messages.error(request, "Connection Error Occured")
            return render(request, 'checkout.html')
        order = Order(
            user=request.user,
            fullname=fullname,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            payment_method=payment_method,
            products=get_cart_products(request.user)
        )
        order.save()
        
        return redirect('index')

    return render(request, 'checkout.html')

def get_cart_products(user):
    cart_items = Cart.objects.filter(user=user)
    products = {}
    for item in cart_items:
        products[item.product.id] = item.quantity
    return json.dumps(products)

def shop_view(request):
    products = Product.objects.all()
    
    return render(request, 'shop.html', {'products': products})



@login_required(login_url='/login/')
def add_to_cart_byID(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart.quantity += 1
        cart.save()
    return redirect('cart_view')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            contact_message = ContactMessage(
                name=name,
                email=email,
                message=message
            )
            contact_message.save()
            return redirect('contact_view')
    
    return render(request, 'contact.html')


def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})


def remove_item_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, 'Item removed from the cart.')
        return redirect('cart_view')  
    
    return redirect('cart_view') 


def cart_item_count(request):
    total_items = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({'total_items': total_items})