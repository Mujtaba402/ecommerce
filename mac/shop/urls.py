from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ShopHome'),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='ContactUs'),
    path('tracker/', views.tracker, name='TrakingStatus'),
    path('checkout/', views.checkout, name='Checkout'),
    path('search/', views.search, name='Search'),
    path('products/<int:myid>', views.productView, name='ProdView'),
    path('signup', views.handleSignUp, name='SignUp'),
    path('login', views.handleLogin, name='Login'),
    path('logout', views.handleLogout, name='Logout'),
]
