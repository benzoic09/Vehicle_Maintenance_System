from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from .models import Product
from django.core.mail import send_mail

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def services(request):
    products = Product.objects.all()
    total = 0
    selected_products = []

    if request.method == 'POST':
        selected_ids = request.POST.getlist('products')
        selected_products = Product.objects.filter(id__in=selected_ids)
        total = sum(product.price for product in selected_products)

        if request.POST.get('action') == 'send_email':
            subject = 'Selected Products'
            message = '\n'.join(f'{product.name} - ${product.price}' for product in selected_products)
            recipient = request.user.email  # Send email to the logged-in user
            # recipient = 'benzoic09@hotmail.com'
            send_mail(subject, message, 'gichimumbugua@gmail.com', [recipient])
            return render(request, 'email_sent.html')  # Ensure email_sent.html exists

    return render(request, 'services.html', {'products': products, 'total': total, 'selected_products': selected_products})

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('services')  # Redirect to services after login
        else:
            # Return an 'invalid login' error message.
            pass
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def product_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        if name and price:  # Add a check to ensure both fields are filled
            Product.objects.create(name=name, price=price)
        return redirect('product_list')
    
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.save()
        return redirect('product_list')
    return render (request, 'edit_product.html', {product: product})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})
