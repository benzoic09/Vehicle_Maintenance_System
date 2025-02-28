from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ProductForm, Appointmentform
from .models import Product, Appointment
from django.core.mail import send_mail
from django.conf import settings


def is_admin_or_superuser(user):
    return user.is_authenticated and (user.is_admin or user.is_staff or user.is_superuser)

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def services(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    total = 0
    selected_products = []

    if request.method == 'POST':
        selected_ids = request.POST.getlist('products')
        selected_products = Product.objects.filter(id__in=selected_ids)
        total = sum(product.price for product in selected_products)
        
        if request.POST.get('action') == 'send_email':
            subject = 'Your Invoice for Selected Products'
            message = "Here's your invoice:\n\n"
            message += '\n'.join(f'{product.name} - KES{product.price}' for product in selected_products)
            message += f'\n\nTotal: KES{total}'
            recipient = request.user.email  # Send email to the logged-in user

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient],
                    fail_silently=False,
                )
                return render(request, 'email_sent.html', {
                    'selected_products': selected_products,
                    'total': total
                })
            except Exception as e:
                # Log the error and show an error message to the user
                error_message = str(e)
                print(f"Error sending email: {error_message}")
                return render(request, 'email_error.html', {
                    'error_message': error_message,
                    'selected_products': selected_products,
                    'total': total
                })

    context = {
        'products': products,
        'total': total,
        'selected_products': selected_products
    }
    return render(request, 'services.html', context)

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
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    # products = Product.objects.all()
    return render(request, 'products.html', {'products': products, 'form': form})

@user_passes_test(is_admin_or_superuser)
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

@user_passes_test(is_admin_or_superuser)
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
            return redirect('schedule_appointment')
    else:
        form = Appointmentform()
        appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments, 'form': form})
