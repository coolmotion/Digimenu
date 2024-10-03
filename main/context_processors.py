from .models import Profile,Menu
from django.shortcuts import get_object_or_404


# Create context processor so our cart can work on all pages of the site
def cart(request):
	# Return the default data from our Cart
	return {'cart': Cart(request)}

def resturant(request):
    resturant_id = request.resolver_match.kwargs.get('resturant_id', None)
    if resturant_id:
        profile = get_object_or_404(Profile, id=resturant_id)
        menus = Menu.objects.filter(user=profile.user)
        return {
            'menus': menus,
            'resturant': profile,
        }
    return {}