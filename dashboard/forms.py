from django import forms
from django.forms import inlineformset_factory
from main.models import Product, Portion, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'menu', 'description', 'image', 'stock', 'is_available']
    
    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if user_profile:
            self.fields['menu'].queryset = Category.objects.filter(resturant=user_profile)

# Formset for Portion
PortionFormSet = inlineformset_factory(Product, Portion, fields=['name', 'price', 'size'], extra=1)
