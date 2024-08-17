from django.shortcuts import render

# Create your views here.
def index(request):
    # categories = Category.objects.all()
    return render(request, 'index.html', )
