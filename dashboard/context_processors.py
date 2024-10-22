from main.models import Profile
from django.shortcuts import get_object_or_404

def profile(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        return {"profile": profile}
    else:
        return {}  # Return an empty context or default values as needed
