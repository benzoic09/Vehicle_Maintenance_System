from django.core.mail import send_mail
from django.conf import settings

def send_cart_email(user_email, cart_items):
    subject = 'Your Cart Update'
    message = f'You have added new items to your cart:\n\n'
    for item in cart_items:
        message += f'- {item.product.name}: {item.quantity}\n'
    message += '\nThank you for shopping with us!'
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )