from django.db import models
from django.conf import settings
from config.models import BasedModel
from .managers import UserManager
from django.contrib.auth.models import AbstractUser

class User(AbstractUser, BasedModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email
    
class Category(BasedModel):
    name = models.CharField(max_length=255) 
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name
    

class Product(BasedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.category.name}'
    

class Cart(BasedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return f"{self.product.name}x{self.quantity} in {self.user.email}'s cart"
    


class Order(BasedModel):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card Payment'),
        ('cash', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='card')
    products = models.JSONField() 

    def __str__(self):
        return f"Order by {self.fullname} ({self.email})"
    

class ContactMessage(BasedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name} ({self.email})"