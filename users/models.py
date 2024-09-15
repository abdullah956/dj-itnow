from django.db import models
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
    