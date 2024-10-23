from main.models import Profile, Category
from django.shortcuts import get_object_or_404

def profile(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        categories = Category.objects.filter(resturant=profile)

        return {"profile": profile, "menus": categories}
    else:
        return {}  # Return an empty context or default values as needed
