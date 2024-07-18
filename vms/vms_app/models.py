from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add any additional fields you need

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/',null=True, blank=True )

    def __str__(self):
        return self.name
    
user = get_user_model()
class Appointment(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='appointments')
    vehicle = models.CharField(max_length=100)
    vehicle = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')])

    def __str__(self):
            return f'{self.service.name} - {self.user.username} on {self.date.strftime("%Y-%m-%d %H:%M")}'