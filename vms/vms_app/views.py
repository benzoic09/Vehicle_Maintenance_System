from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ProductForm, Appointmentform
from .models import Product, Appointment
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
            subject = 'Your Invoice for Selected Products'
            message = '\n'.join(f'{product.name} - ${product.price}' for product in selected_products)
            recipient = request.user.email  # Send email to the logged-in user
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
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products, 'form': form})


@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})


@login_required
def schedule_appointment(request):
    if request.method =='POST':
        form = Appointmentform(request.POST)
        if form.is_valid():
            appointment  = form.save(commit=False)
            appointment.user = request.user
            appointment.status = 'scheduled'
            appointment.save()
            return redirect('appointment_list')
        else:
            form = Appointmentform()
        return render(request, 'schedule_appointment.html', {'form': form})


@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})