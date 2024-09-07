from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('thanks/', views.signup_thanks, name='signup_thanks'),
    path('product/', views.product, name='product'),
    path('feature/', views.feature, name='feature'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('userinfo/', views.user_info, name='user_info'),
]
