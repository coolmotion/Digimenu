from django.contrib import admin
from .models import Menu, Product, Profile
from django.contrib.auth.models import User

class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    # list_display = ('name', 'user')
    inlines = [ProductInline]

admin.site.register(Menu, MenuAdmin)
# admin.site.register(Product)  

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)