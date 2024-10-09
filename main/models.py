from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    resturant_name = models.CharField(max_length=200, blank=True)
    resturant_slogan = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='uploads/product/', blank=True, null=True)
    description = models.CharField(max_length=400, default='0', blank=True, null=True)
    city = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.resturant_name

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile creation
post_save.connect(create_profile, sender=User)

class Category(models.Model):
    resturant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name.capitalize()

class Product(models.Model):
    name = models.CharField(max_length=100)
    resturant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    menu = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='0', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)  # Field to track product availability

    def __str__(self):
        return f"{self.resturant.resturant_name} - {self.name}"

class Portion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='portions')
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.product} - {self.name}"
