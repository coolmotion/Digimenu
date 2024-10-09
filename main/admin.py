from django.contrib import admin
from .models import Category, Product, Portion, Profile
from django.contrib.auth.models import User

# Define an inline admin descriptor for Portion model
# which acts a bit like a singleton
class PortionInline(admin.TabularInline):  # Using TabularInline for a more compact display
    model = Portion
    extra = 1  # Number of extra forms to display

# Define the admin class for Product
class ProductAdmin(admin.ModelAdmin):
    inlines = (PortionInline,)  # Add Portion inline here

class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    # list_display = ('name', 'user')
    inlines = [ProductInline]

# Register the Admin classes for Menu using the decorator
admin.site.register(Category, MenuAdmin)
admin.site.register(Product, ProductAdmin)  # Updated registration

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]  # It should be 'fields' not 'field'
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)
