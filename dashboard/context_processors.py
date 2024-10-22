from main.models import Profile
from django.shortcuts import get_object_or_404

def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return { "profile":profile}