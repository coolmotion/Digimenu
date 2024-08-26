from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	resturant_name = models.CharField(max_length=200, blank=True)
	resturant_slogan = models.CharField(max_length=200, blank=True)
	image = models.ImageField(upload_to='uploads/product/',blank=True, null=True )
	description = models.CharField(max_length=400, default='0', blank=True, null=True)
	city = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return self.user.username
	
# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)

class Menu(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)

	def __str__(self):
		profile = Profile.objects.get(user=self.user)  # Get the Profile associated with the User
		restaurant_name = profile.resturant_name.capitalize()  # Capitalize the restaurant name
		menu_name = self.name.capitalize()  # Capitalize the menu name
		return f"{restaurant_name} {menu_name}"

         



class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='0', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/',blank=True, null=True )
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

	def __str__(self):
		return f"{self.name} {self.menu}"

